"""
Project Configuration & Industry Profile Model
==============================================
Defines the standard profile contract for generic SEO swarm audits across:
- Generic Web & Lead Gen
- B2B SaaS & Software Platforms
- Local Services & Trades
- Ecommerce & Retail
- Publishers & Media
"""

import os
import json
import re
from typing import Dict, List, Any, Optional

DEFAULT_GENERIC_PROFILE: Dict[str, Any] = {
    "profile_id": "generic_web",
    "brand_name": "Generic Website",
    "site_url": "https://example.com",
    "industry": "generic",
    "target_scope": "national",
    "target_locations": [],
    "target_languages": ["en"],
    "business_model": "lead_gen",
    "required_signals": ["contact_or_action", "privacy_and_terms"],
    "active_personas": ["comparison_shopper", "mobile_first_customer", "information_gain_critic"],
    "codebase": {
        "framework": "auto",
        "extensions": [".html", ".htm", ".php", ".jsx", ".tsx", ".vue", ".astro"]
    }
}

LOCAL_SERVICES_PROFILE: Dict[str, Any] = {
    "profile_id": "local_services",
    "brand_name": "Local Service Contractor",
    "site_url": "https://example-contractor.com",
    "industry": "local_services",
    "target_scope": "local",
    "target_locations": [],
    "target_languages": ["en"],
    "business_model": "local_calls_estimates",
    "required_signals": ["tap_to_call", "service_area", "ownership_or_trust_guarantee"],
    "active_personas": ["skeptical_contractor", "mobile_first_customer", "local_seo_tech_specialist"],
    "codebase": {
        "framework": "auto",
        "extensions": [".html", ".htm", ".php", ".jsx", ".tsx", ".vue", ".astro"]
    }
}

SAAS_PROFILE: Dict[str, Any] = {
    "profile_id": "b2b_saas",
    "brand_name": "B2B SaaS Platform",
    "site_url": "https://example-saas.com",
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

ECOMMERCE_PROFILE: Dict[str, Any] = {
    "profile_id": "ecommerce",
    "brand_name": "Online Retail Store",
    "site_url": "https://example-shop.com",
    "industry": "ecommerce",
    "target_scope": "national",
    "target_locations": [],
    "target_languages": ["en"],
    "business_model": "direct_checkout",
    "required_signals": ["add_to_cart_or_buy", "pricing_transparency", "shipping_and_returns"],
    "active_personas": ["comparison_shopper", "mobile_first_customer", "schema_specialist"],
    "codebase": {
        "framework": "auto",
        "extensions": [".html", ".htm", ".php", ".jsx", ".tsx", ".vue", ".astro"]
    }
}

PROFILE_REGISTRY = {
    "generic": DEFAULT_GENERIC_PROFILE,
    "generic_web": DEFAULT_GENERIC_PROFILE,
    "local_services": LOCAL_SERVICES_PROFILE,
    "saas": SAAS_PROFILE,
    "b2b_saas": SAAS_PROFILE,
    "ecommerce": ECOMMERCE_PROFILE
}

def _parse_yaml_basic(content: str) -> Dict[str, Any]:
    """Lightweight zero-dependency YAML parser supporting nested mappings, lists, and primitives."""
    res: Dict[str, Any] = {}
    lines = content.splitlines()
    
    current_section = None
    current_key = None
    
    for raw_line in lines:
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
            
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        
        # Check list item
        if stripped.startswith("- "):
            item_val = stripped[2:].strip().strip("\"'")
            if indent >= 2 and current_section and current_key and current_key != current_section:
                # Sub-list under a section (e.g. codebase.extensions)
                if not isinstance(res.get(current_section), dict):
                    res[current_section] = {}
                if not isinstance(res[current_section].get(current_key), list):
                    res[current_section][current_key] = []
                res[current_section][current_key].append(item_val)
            else:
                # Top level list
                target_key = current_key or current_section
                if target_key:
                    if not isinstance(res.get(target_key), list):
                        res[target_key] = []
                    res[target_key].append(item_val)
            continue

        if ":" in stripped:
            parts = stripped.split(":", 1)
            k = parts[0].strip()
            v = parts[1].strip()
            
            if indent >= 2 and current_section:
                # Child key of section
                current_key = k
                if not isinstance(res.get(current_section), dict):
                    res[current_section] = {}
                if v == "" or v == "[]":
                    res[current_section][k] = [] if v == "[]" else {}
                elif v == "{}":
                    res[current_section][k] = {}
                elif v.lower() == "true":
                    res[current_section][k] = True
                elif v.lower() == "false":
                    res[current_section][k] = False
                elif v.isdigit():
                    res[current_section][k] = int(v)
                else:
                    res[current_section][k] = v.strip("\"'")
            else:
                # Top level key
                current_section = k if v == "" else None
                current_key = k
                if v == "":
                    # If this is followed by lists or dicts, don't set scalar
                    pass
                elif v == "[]":
                    res[k] = []
                elif v == "{}":
                    res[k] = {}
                elif v.lower() == "true":
                    res[k] = True
                elif v.lower() == "false":
                    res[k] = False
                elif v.isdigit():
                    res[k] = int(v)
                else:
                    res[k] = v.strip("\"'")

    return res

def load_project_profile(profile_path_or_id: Optional[str] = None) -> Dict[str, Any]:
    """Loads a project profile from JSON/YAML or resolves a built-in profile ID.
    Fails loudly with ValueError if the specified file does not exist or is invalid."""
    import copy
    if not profile_path_or_id or profile_path_or_id == "generic":
        return copy.deepcopy(DEFAULT_GENERIC_PROFILE)
        
    if profile_path_or_id in PROFILE_REGISTRY:
        return copy.deepcopy(PROFILE_REGISTRY[profile_path_or_id])
        
    if not os.path.exists(profile_path_or_id):
        raise FileNotFoundError(f"Profile configuration file '{profile_path_or_id}' not found.")
        
    with open(profile_path_or_id, "r", encoding="utf-8") as f:
        content = f.read()

    data: Dict[str, Any] = {}
    if profile_path_or_id.endswith(".json"):
        try:
            data = json.loads(content)
        except Exception as e:
            raise ValueError(f"Malformed JSON in profile '{profile_path_or_id}': {e}")
    elif profile_path_or_id.endswith((".yaml", ".yml")):
        data = _parse_yaml_basic(content)
        if not data:
            raise ValueError(f"Failed to parse YAML profile '{profile_path_or_id}'.")
    else:
        # Attempt JSON then fallback to basic YAML
        try:
            data = json.loads(content)
        except Exception:
            data = _parse_yaml_basic(content)
            if not data:
                raise ValueError(f"Profile file '{profile_path_or_id}' is neither valid JSON nor YAML.")

    if not isinstance(data, dict):
        raise ValueError("Profile schema validation error: root must be a dictionary/mapping.")

    if "active_personas" in data and not isinstance(data["active_personas"], list):
        raise ValueError("Profile schema validation error: 'active_personas' must be a list.")

    # Deep merge with default profile
    merged = copy.deepcopy(DEFAULT_GENERIC_PROFILE)
    for k, v in data.items():
        if k == "codebase" and isinstance(v, dict):
            merged["codebase"] = {**merged.get("codebase", {}), **v}
        else:
            merged[k] = v

    if not merged.get("profile_id"):
        raise ValueError("Profile schema validation error: 'profile_id' is required.")
        
    return merged
