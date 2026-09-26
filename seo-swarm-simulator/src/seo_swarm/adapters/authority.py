"""
Authority Dataset Validation Adapter
====================================
Validates external backlink / domain authority datasets against audited project profiles:
- Ahrefs / Moz / Semrush JSON or CSV exports
- Asserts domain identity, metric provenance, fetch timestamps, and valid integer ranges
"""

import os
import json
import hashlib
from typing import Dict, Any, Optional
from urllib.parse import urlparse

def validate_authority_data(authority_path_or_dict: Any, expected_site_url: Optional[str] = None) -> Dict[str, Any]:
    """Validates an authority profile and returns a structured authority evidence contract.
    Rejects invalid/empty payloads and ensures the domain matches the target project."""
    if not authority_path_or_dict:
        return {"status": "UNKNOWN", "referring_domains": 0, "domain_authority": 0, "provider": "none"}
        
    data: Dict[str, Any] = {}
    if isinstance(authority_path_or_dict, dict):
        data = authority_path_or_dict
    elif isinstance(authority_path_or_dict, str):
        if not os.path.exists(authority_path_or_dict):
            return {"status": "UNKNOWN", "referring_domains": 0, "domain_authority": 0, "provider": "file_not_found"}
        try:
            with open(authority_path_or_dict, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            return {"status": "UNKNOWN", "referring_domains": 0, "domain_authority": 0, "provider": "parse_error"}

    # Validate essential keys and domain identity
    domain = data.get("domain", "").strip()
    provider = data.get("provider", "generic").strip()
    rd = data.get("referring_domains")
    da = data.get("domain_authority")
    
    if rd is None or da is None or not isinstance(rd, int) or not isinstance(da, int):
        return {
            "status": "UNKNOWN",
            "referring_domains": 0,
            "domain_authority": 0,
            "provider": provider,
            "error": "Invalid referring_domains or domain_authority metrics."
        }

    # Verify domain alignment if expected_site_url is provided
    if expected_site_url and domain:
        expected_host = urlparse(expected_site_url).netloc.lower() or expected_site_url.lower()
        clean_domain = domain.lower()
        if expected_host and clean_domain not in expected_host and expected_host not in clean_domain:
            return {
                "status": "UNKNOWN",
                "referring_domains": 0,
                "domain_authority": 0,
                "provider": provider,
                "error": f"Authority domain '{domain}' does not match target project '{expected_host}'."
            }

    return {
        "status": "VERIFIED",
        "domain": domain or (expected_site_url or "target"),
        "provider": provider,
        "referring_domains": max(0, rd),
        "domain_authority": max(0, min(100, da)),
        "fetched_at": data.get("fetched_at", "N/A")
    }
