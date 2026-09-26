"""
Project Configuration & Industry Profile Model
==============================================
Defines the standard profile contract for generic SEO swarm audits across:
- Generic SaaS & B2B
- Local Trades & Home Services (Roofing, HVAC, Plumbing)
- Ecommerce & Retail
- Publishers & Editorial
- Enterprise & Technical Docs
"""

import os
import json
from typing import Dict, List, Any, Optional

DEFAULT_GENERIC_PROFILE: Dict[str, Any] = {
    "profile_id": "generic_web",
    "brand_name": "Generic Website",
    "industry": "generic",
    "target_scope": "national",
    "target_locations": [],
    "target_languages": ["en"],
    "business_model": "lead_gen",
    "required_signals": ["contact_or_action", "privacy_and_terms"],
    "active_personas": ["comparison_shopper", "mobile_first_customer", "information_gain_critic"],
    "codebase": {
        "framework": "auto",
        "extensions": [".html", ".php", ".jsx", ".tsx", ".vue", ".astro"]
    }
}

LOCAL_SERVICES_PROFILE: Dict[str, Any] = {
    "profile_id": "local_trades_home_services",
    "brand_name": "Local Contractor / Service",
    "industry": "local_services",
    "target_scope": "local",
    "target_locations": ["Tyler", "Waco", "Dallas", "Houston", "San Angelo", "Katy", "The Woodlands", "Sugar Land"],
    "target_languages": ["en"],
    "business_model": "local_calls_estimates",
    "required_signals": ["tap_to_call", "service_area", "ownership_or_trust_guarantee"],
    "active_personas": ["skeptical_contractor", "mobile_first_customer", "local_seo_tech_specialist"],
    "codebase": {
        "framework": "auto",
        "extensions": [".php", ".html"]
    }
}

SAAS_PROFILE: Dict[str, Any] = {
    "profile_id": "b2b_saas_software",
    "brand_name": "B2B SaaS Platform",
    "industry": "saas",
    "target_scope": "global",
    "target_locations": [],
    "target_languages": ["en"],
    "business_model": "subscriptions_demos",
    "required_signals": ["free_trial_or_demo", "pricing_transparency", "api_documentation"],
    "active_personas": ["comparison_shopper", "technical_buyer", "information_gain_critic"],
    "codebase": {
        "framework": "auto",
        "extensions": [".tsx", ".jsx", ".html", ".vue", ".astro", ".php"]
    }
}

PROFILE_REGISTRY = {
    "generic": DEFAULT_GENERIC_PROFILE,
    "local_services": LOCAL_SERVICES_PROFILE,
    "roofing": LOCAL_SERVICES_PROFILE,
    "saas": SAAS_PROFILE
}

def load_project_profile(profile_path_or_id: Optional[str] = None) -> Dict[str, Any]:
    """Loads a project profile from JSON/YAML or resolves a built-in profile ID."""
    if not profile_path_or_id:
        return dict(DEFAULT_GENERIC_PROFILE)
        
    if profile_path_or_id in PROFILE_REGISTRY:
        return dict(PROFILE_REGISTRY[profile_path_or_id])
        
    if os.path.exists(profile_path_or_id):
        try:
            with open(profile_path_or_id, "r", encoding="utf-8") as f:
                # Support JSON format by default
                data = json.load(f)
                return {**DEFAULT_GENERIC_PROFILE, **data}
        except Exception:
            pass
            
    return dict(DEFAULT_GENERIC_PROFILE)
