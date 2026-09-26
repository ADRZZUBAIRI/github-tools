import pytest
import os
from seo_swarm.roles.roster import ALL_62_ROLES, get_active_roles, TASK_ACTIVATION_PRESETS
from seo_swarm.ingest.gsc_ingest import GSCDataIngestor
from seo_swarm.analysis.decision_gate import apply_hard_reality_caps

def test_unimplemented_roles_score_zero():
    """Ensure unimplemented roles do not default to 75 and return status not_implemented."""
    unimplemented = [r for r in ALL_62_ROLES if not r.is_implemented]
    assert len(unimplemented) > 30
    
    page_data = {"url": "test.php", "title": "Test Title", "html": "<p>test</p>", "text": "test"}
    evidence_map = {}
    
    for r in unimplemented:
        res = r.evaluate(page_data, evidence_map)
        assert res["status"] == "not_implemented"
        assert res["score"] == 0.0

def test_missing_gsc_caps_score_at_20():
    """P0 Invariant: When GSC is not loaded, final score is hard-capped at 20 with GSC_DATA_REQUIRED."""
    raw_score = 65.0
    site_gsc = {"is_active": False, "status": "NOT_LOADED"}
    page_gsc = None
    authority_data = {"status": "UNKNOWN", "referring_domains": 0, "domain_authority": 0}
    commercial_data = {"has_tap_to_call": True, "has_ownership_guarantee": True}
    
    decision = apply_hard_reality_caps(
        raw_score=raw_score,
        gsc_metrics=site_gsc,
        page_metrics=page_gsc,
        authority_data=authority_data,
        commercial_data=commercial_data,
        is_national_target=False
    )
    
    assert decision["final_capped_score"] <= 20.0
    assert decision["verdict"] == "GSC_DATA_REQUIRED"
    assert any("GSC DATA REQUIRED GATE" in r for r in decision["cap_reasons"])

def test_gsc_28_day_low_visibility_caps_at_10():
    """P0 Invariant: A verified 28+ day dataset with <500 impressions and 0 clicks caps at 10.0/100."""
    raw_score = 70.0
    site_gsc = {
        "is_active": True,
        "complete_days": 28,
        "window_start": "2026-08-01",
        "window_end": "2026-08-28",
        "total_impressions": 65,
        "total_clicks": 0,
        "tracked_pages_count": 186
    }
    page_gsc = {"clicks": 0, "impressions": 5, "position": 85.0}
    authority_data = {"status": "VERIFIED", "referring_domains": 2, "domain_authority": 5}
    commercial_data = {"has_tap_to_call": True, "has_ownership_guarantee": True}
    
    decision = apply_hard_reality_caps(
        raw_score=raw_score,
        gsc_metrics=site_gsc,
        page_metrics=page_gsc,
        authority_data=authority_data,
        commercial_data=commercial_data,
        is_national_target=False
    )
    
    assert decision["final_capped_score"] == 10.0
    assert decision["verdict"] == "CRITICAL_ACQUISITION_FAILURE"

def test_unverified_authority_caps_at_30():
    """P0 Invariant: Unverified authority datasets must be capped at 30 without claiming 0 links."""
    raw_score = 65.0
    site_gsc = {
        "is_active": True,
        "complete_days": 28,
        "window_start": "2026-08-01",
        "window_end": "2026-08-28",
        "total_impressions": 5000,
        "total_clicks": 150,
        "tracked_pages_count": 50
    }
    authority_data = {"status": "UNKNOWN", "referring_domains": 0, "domain_authority": 0}
    commercial_data = {"has_tap_to_call": True, "has_ownership_guarantee": True}
    
    decision = apply_hard_reality_caps(
        raw_score=raw_score,
        gsc_metrics=site_gsc,
        page_metrics=None,
        authority_data=authority_data,
        commercial_data=commercial_data,
        is_national_target=False
    )
    
    assert decision["final_capped_score"] <= 30.0
    assert any("UNVERIFIED AUTHORITY GATE" in r for r in decision["cap_reasons"])
