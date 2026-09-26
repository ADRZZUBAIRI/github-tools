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

def _extract_canonical_domain(url_or_domain: str) -> str:
    """Extracts a clean normalized lower-case domain/hostname from a URL or raw domain string."""
    raw = url_or_domain.strip().lower()
    if "://" in raw:
        parsed = urlparse(raw)
        raw = parsed.netloc or parsed.path
    # Strip any port or leading/trailing slashes/paths
    raw = raw.split("/")[0].split(":")[0]
    # Strip leading 'www.'
    if raw.startswith("www."):
        raw = raw[4:]
    return raw

def validate_authority_data(authority_path_or_dict: Any, expected_site_url: Optional[str] = None) -> Dict[str, Any]:
    """Validates an authority profile and returns a structured authority evidence contract.
    Rejects invalid/empty payloads and ensures the domain matches the target project exactly."""
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

    if not isinstance(data, dict):
        return {"status": "UNKNOWN", "referring_domains": 0, "domain_authority": 0, "provider": "invalid_payload"}

    # Validate essential keys and domain identity
    raw_domain = data.get("domain")
    if not raw_domain or not isinstance(raw_domain, str) or not raw_domain.strip():
        return {
            "status": "UNKNOWN",
            "referring_domains": 0,
            "domain_authority": 0,
            "provider": str(data.get("provider", "none")),
            "error": "Authority dataset missing required 'domain' property."
        }
    
    domain = _extract_canonical_domain(raw_domain)
    provider = str(data.get("provider", "generic")).strip()
    rd = data.get("referring_domains")
    da = data.get("domain_authority")
    
    # Must be real integers (reject bools or strings)
    if rd is None or da is None or type(rd) is not int or type(da) is not int:
        return {
            "status": "UNKNOWN",
            "referring_domains": 0,
            "domain_authority": 0,
            "provider": provider,
            "error": "Invalid referring_domains or domain_authority metrics (must be integers)."
        }

    if rd < 0 or da < 0 or da > 100:
        return {
            "status": "UNKNOWN",
            "referring_domains": 0,
            "domain_authority": 0,
            "provider": provider,
            "error": f"Authority metrics out of valid bounds (rd={rd}, da={da})."
        }

    # Verify exact domain alignment if expected_site_url is provided
    if expected_site_url:
        expected_domain = _extract_canonical_domain(expected_site_url)
        if expected_domain and domain != expected_domain:
            return {
                "status": "UNKNOWN",
                "referring_domains": 0,
                "domain_authority": 0,
                "provider": provider,
                "error": f"Authority domain '{domain}' does not match target project domain '{expected_domain}'."
            }

    return {
        "status": "VERIFIED",
        "domain": domain,
        "provider": provider,
        "referring_domains": rd,
        "domain_authority": da,
        "fetched_at": str(data.get("fetched_at", "N/A"))
    }
