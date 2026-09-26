import pytest
import os
import json
import tempfile
from seo_swarm.roles.roster import ALL_62_ROLES, get_active_roles, TASK_ACTIVATION_PRESETS
from seo_swarm.ingest.gsc_ingest import GSCDataIngestor
from seo_swarm.analysis.decision_gate import apply_hard_reality_caps
from seo_swarm.config.profile import load_project_profile, DEFAULT_GENERIC_PROFILE, SAAS_PROFILE, LOCAL_SERVICES_PROFILE
from seo_swarm.adapters.codebase import extract_page_primitives, normalize_route_path, discover_public_codebase_routes
from seo_swarm.adapters.authority import validate_authority_data
from seo_swarm.adapters.serp import load_serp_snapshot

# ==============================================================================
# 1. CORE UNINFLATED SCORING & GATING TESTS
# ==============================================================================
def test_unimplemented_roles_score_zero():
    """Ensure unimplemented roles return status not_implemented and 0.0 score."""
    unimplemented = [r for r in ALL_62_ROLES if not r.is_implemented]
    assert len(unimplemented) > 35
    
    page_data = {"url": "test.html", "title": "Test Title", "html": "<p>test</p>", "text": "test"}
    evidence_map = {}
    
    for r in unimplemented:
        res = r.evaluate(page_data, evidence_map)
        assert res["status"] == "not_implemented"
        assert res["score"] == 0.0

def test_missing_gsc_caps_score_at_20():
    """Missing GSC data must hard-cap the score at <= 20.0 with GSC_DATA_REQUIRED."""
    raw_score = 75.0
    site_gsc = {"is_active": False, "status": "NOT_LOADED"}
    decision = apply_hard_reality_caps(
        raw_score=raw_score,
        gsc_metrics=site_gsc,
        page_metrics=None,
        authority_data={"status": "UNKNOWN"},
        commercial_data={"has_tap_to_call": True, "has_ownership_guarantee": True},
        is_national_target=False
    )
    assert decision["final_capped_score"] <= 20.0
    assert decision["verdict"] == "GSC_DATA_REQUIRED"

def test_gsc_28_day_low_visibility_caps_at_10():
    """Verified 28+ day dataset with <500 impressions and 0 clicks must cap at 10.0/100."""
    site_gsc = {
        "is_active": True,
        "complete_days": 28,
        "window_start": "2026-08-01",
        "window_end": "2026-08-28",
        "total_impressions": 65,
        "total_clicks": 0,
        "tracked_pages_count": 186
    }
    decision = apply_hard_reality_caps(
        raw_score=68.0,
        gsc_metrics=site_gsc,
        page_metrics={"clicks": 0, "impressions": 5, "position": 85.0},
        authority_data={"status": "VERIFIED", "referring_domains": 5, "domain_authority": 10},
        commercial_data={"has_tap_to_call": True, "has_ownership_guarantee": True},
        is_national_target=False
    )
    assert decision["final_capped_score"] == 10.0
    assert decision["verdict"] == "CRITICAL_ACQUISITION_FAILURE"

def test_unverified_authority_caps_at_30():
    """Unverified authority profile must be capped at <= 30.0."""
    decision = apply_hard_reality_caps(
        raw_score=70.0,
        gsc_metrics={"is_active": True, "complete_days": 28, "total_impressions": 1500, "total_clicks": 50},
        page_metrics=None,
        authority_data={"status": "UNKNOWN"},
        commercial_data={"has_tap_to_call": True, "has_ownership_guarantee": True},
        is_national_target=False
    )
    assert decision["final_capped_score"] <= 30.0

# ==============================================================================
# 2. PROFILE & YAML/JSON PARSING TESTS
# ==============================================================================
def test_built_in_profiles_resolution():
    """Ensure generic, saas, and local_services built-in profiles resolve accurately."""
    p_generic = load_project_profile("generic")
    assert p_generic["industry"] == "generic"
    assert "information_gain_critic" in p_generic["active_personas"]
    
    p_saas = load_project_profile("saas")
    assert p_saas["industry"] == "saas"
    assert "technical_buyer" in p_saas["active_personas"]
    
    p_local = load_project_profile("local_services")
    assert p_local["industry"] == "local_services"
    assert p_local["target_scope"] == "local"

def test_yaml_profile_loading():
    """Verify loading custom YAML profile configuration."""
    yaml_content = """
profile_id: custom_ecommerce
brand_name: Test Store
industry: ecommerce
target_scope: national
target_languages:
  - en
  - es
required_signals:
  - add_to_cart
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as tf:
        tf.write(yaml_content)
        tf_path = tf.name
        
    try:
        loaded = load_project_profile(tf_path)
        assert loaded["profile_id"] == "custom_ecommerce"
        assert loaded["industry"] == "ecommerce"
        assert "es" in loaded["target_languages"]
    finally:
        os.remove(tf_path)

def test_invalid_profile_raises_error():
    """Ensure malformed or non-existent profile files raise explicit errors without silent fallback."""
    with pytest.raises(FileNotFoundError):
        load_project_profile("non_existent_profile_path.yaml")

# ==============================================================================
# 3. UNIVERSAL CODEBASE & MULTI-FRAMEWORK ADAPTER TESTS
# ==============================================================================
def test_codebase_multi_framework_extraction():
    """Extract primitives from HTML, PHP, JSX/TSX, Vue, and Astro templates."""
    # 1. Next.js / React TSX
    with tempfile.NamedTemporaryFile(mode="w", suffix=".tsx", delete=False) as tf:
        tf.write("export const metadata = { title: 'Enterprise Cloud SaaS' }; export default function Page() { return <h1>Platform</h1>; }")
        tsx_path = tf.name
    try:
        res = extract_page_primitives(tsx_path)
        assert res["framework"] == "react_nextjs"
        assert "Enterprise Cloud SaaS" in res["title"]
    finally:
        os.remove(tsx_path)

    # 2. PHP Server Template
    with tempfile.NamedTemporaryFile(mode="w", suffix=".php", delete=False) as tf:
        tf.write("<?php $page_title = 'Custom Middleware API'; ?> <p>Content</p>")
        php_path = tf.name
    try:
        res = extract_page_primitives(php_path)
        assert res["framework"] == "php_native"
        assert res["title"] == "Custom Middleware API"
    finally:
        os.remove(php_path)

def test_route_normalization():
    """Test URL route normalization and canonical mappings."""
    route_info = normalize_route_path("c:/sites/app/pages/pricing/index.html", "c:/sites/app", "https://mysaas.com")
    assert route_info["route"] == "/pages/pricing"
    assert route_info["public_url"] == "https://mysaas.com/pages/pricing"

# ==============================================================================
# 4. AUTHORITY VALIDATION ADAPTER TESTS
# ==============================================================================
def test_authority_validation_with_domain_match():
    """Valid authority data matching target site URL returns VERIFIED status."""
    auth_payload = {
        "domain": "acme.com",
        "provider": "ahrefs",
        "referring_domains": 120,
        "domain_authority": 45,
        "fetched_at": "2026-09-26T00:00:00Z"
    }
    validated = validate_authority_data(auth_payload, expected_site_url="https://acme.com")
    assert validated["status"] == "VERIFIED"
    assert validated["referring_domains"] == 120
    assert validated["domain_authority"] == 45

def test_authority_domain_mismatch_rejected():
    """Authority dataset for a different domain must be rejected as UNKNOWN."""
    auth_payload = {
        "domain": "competitor.com",
        "provider": "ahrefs",
        "referring_domains": 500,
        "domain_authority": 70
    }
    validated = validate_authority_data(auth_payload, expected_site_url="https://mybrand.com")
    assert validated["status"] == "UNKNOWN"
    assert "does not match" in validated.get("error", "")

# ==============================================================================
# 5. SERP COMPETITOR SNAPSHOT & INFORMATION GAIN TESTS
# ==============================================================================
def test_serp_snapshot_loading():
    """Validate loading competitive SERP snapshot dataset."""
    serp_payload = {
        "target_query": "b2b crm webhook middleware",
        "keyword_difficulty": 42,
        "search_volume": 1200,
        "has_ai_overview": True,
        "top_competitors": ["https://comp1.com", "https://comp2.com"]
    }
    snapshot = load_serp_snapshot(serp_payload)
    assert snapshot["is_verified"] is True
    assert snapshot["keyword_difficulty"] == 42
    assert snapshot["competitor_count"] == 2

def test_information_gain_demands_functional_utility():
    """Information gain role must pass pages with interactive JS functions or tables and fail purely static text."""
    from seo_swarm.roles.roster import InformationGainDataCriticRole
    role = InformationGainDataCriticRole()
    
    # 1. Purely descriptive narrative text -> FAIL
    static_page = {"html": "<p>We provide standard cloud hosting services with good uptime.</p>", "text": "hosting services"}
    res_static = role.evaluate(static_page, {})
    assert res_static["score"] <= 30.0
    assert res_static["verdict"] == "DERIVATIVE_CONTENT_RISK"
    
    # 2. Interactive calculation code -> PASS
    interactive_page = {
        "html": "<script>function calculateDowntimeCost(users) { return users * 12.50; }</script><p>Calculator</p>",
        "text": "calculator"
    }
    res_interactive = role.evaluate(interactive_page, {})
    assert res_interactive["score"] >= 85.0
    assert res_interactive["verdict"] == "INFORMATION_GAIN_CONFIRMED"
