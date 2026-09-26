"""
Hard Visibility & Reality Decision Gate
========================================
Implements non-negotiable hard caps based on real performance evidence:
1. GSC Data Missing Gate: Missing GSC data caps score at 20.0/100 (verdict: GSC_DATA_REQUIRED).
2. Critical 28+ Day Visibility Gate: Verified 28+ day low visibility (<500 impr, 0 clicks) caps at 10.0/100.
3. Authority Evidence Gate: Unverified authority caps at 30.0/100 without fabricating zero links.
4. Suicidal National Target Gate: Unverified or DA < 10 domain targeting national KD 70+ terms capped at 15.0/100.
5. Page Graveyard Trap: Page at position > 50 with 0 clicks capped at 25.0/100.
6. Commercial Conversion Gate: Missing required conversion cues (e.g. 1-tap phone action for trades, checkout/demo for SaaS/ecom) capped at 30.0/100.
7. Commercial Trust & Offer Gate: Missing required trust or ownership guarantees capped at 35.0/100.
"""

from typing import Dict, List, Any, Optional

def apply_hard_reality_caps(
    raw_score: float,
    gsc_metrics: Dict[str, Any],
    page_metrics: Optional[Dict[str, Any]],
    authority_data: Dict[str, Any],
    commercial_data: Dict[str, Any],
    is_national_target: bool = False
) -> Dict[str, Any]:
    hard_caps: List[float] = []
    reasons: List[str] = []
    
    # 1. GSC DATA PRESENCE GATE (P0: Missing GSC data must NOT produce false passing scores)
    if not gsc_metrics.get("is_active"):
        hard_caps.append(20.0)
        reasons.append("GSC DATA REQUIRED GATE: No verified Google Search Console export provided. Organic search performance is UNKNOWN. Score hard-capped at 20.0/100.")
    else:
        # 2. GSC 28+ DAY CRITICAL VISIBILITY FAILURE GATE
        complete_days = gsc_metrics.get("complete_days", 0)
        total_clicks = gsc_metrics.get("total_clicks", 0)
        total_impressions = gsc_metrics.get("total_impressions", 0)
        tracked_pages = gsc_metrics.get("tracked_pages_count", 0)
        window_start = gsc_metrics.get("window_start", "N/A")
        window_end = gsc_metrics.get("window_end", "N/A")
        
        if complete_days >= 28:
            if total_impressions < 500 and total_clicks == 0:
                hard_caps.append(10.0)
                reasons.append(
                    f"GSC 28-DAY CRITICAL VISIBILITY FAILURE: Verified {complete_days}-day window ({window_start} to {window_end}) "
                    f"records {total_impressions} total impressions and {total_clicks} clicks across {tracked_pages} pages. "
                    "Organic acquisition is functionally zero."
                )
        elif complete_days > 0:
            if total_clicks == 0:
                hard_caps.append(20.0)
                reasons.append(
                    f"GSC SHORT-WINDOW WARNING ({complete_days} days, {window_start} to {window_end}): "
                    f"{total_impressions} impressions and 0 clicks recorded. Insufficient full 28-day baseline; capped at 20.0/100."
                )

    # 3. PAGE-LEVEL TRAFFIC & RANKING GATE (Only when GSC page metrics are verified)
    if page_metrics:
        p_clicks = page_metrics.get("clicks", 0)
        p_pos = page_metrics.get("position", 0.0)
        if p_pos > 50.0 and p_clicks == 0:
            hard_caps.append(25.0)
            reasons.append(f"PAGE 9 GRAVEYARD TRAP: Verified GSC position {p_pos} with 0 clicks.")
            
    # 4. AUTHORITY DATA GATE (UNKNOWN vs VERIFIED)
    auth_status = authority_data.get("status", "UNKNOWN")
    if auth_status != "VERIFIED":
        hard_caps.append(30.0)
        reasons.append(f"UNVERIFIED AUTHORITY GATE: No verified backlink provider dataset configured ({authority_data.get('provider', 'none')}). Domain authority status is UNKNOWN. Score hard-capped at 30.0/100.")
    else:
        referring_domains = authority_data.get("referring_domains", 0)
        domain_authority = authority_data.get("domain_authority", 0)
        if is_national_target and referring_domains < 5 and domain_authority < 10:
            hard_caps.append(15.0)
            reasons.append(f"SUICIDAL NATIONAL COMPETITION GATE: DA {domain_authority} / {referring_domains} Ref Domains targeting national KD 70+ terms against VC-backed incumbents.")
            
    # 5. COMMERCIAL CONVERSION GATE
    has_tap_to_call = commercial_data.get("has_tap_to_call", True)
    if not has_tap_to_call:
        hard_caps.append(30.0)
        reasons.append("COMMERCIAL ZERO-CONVERSION GATE: Missing required 1-tap phone action for mobile conversion.")
        
    # 6. COMMERCIAL TRUST / OWNERSHIP GATE
    has_trust = commercial_data.get("has_ownership_guarantee", True)
    if not has_trust:
        hard_caps.append(35.0)
        reasons.append("COMMERCIAL TRUST GATE: Required asset ownership or risk-reversal guarantee is missing from commercial offer.")
        
    final_score = min([raw_score] + hard_caps) if hard_caps else raw_score
    
    if not gsc_metrics.get("is_active"):
        verdict = "GSC_DATA_REQUIRED"
    elif final_score <= 15.0:
        verdict = "CRITICAL_ACQUISITION_FAILURE"
    elif final_score <= 30.0:
        verdict = "AUTHORITY_OR_EVIDENCE_RESTRICTED"
    elif final_score <= 50.0:
        verdict = "STRIKING_DISTANCE_RESTRICTED"
    elif final_score <= 70.0:
        verdict = "VIABLE_LOCAL_TARGET"
    else:
        verdict = "PRODUCTION_VERIFIED"
    
    return {
        "raw_score": raw_score,
        "final_capped_score": round(final_score, 1),
        "hard_caps_applied": hard_caps,
        "cap_reasons": reasons,
        "verdict": verdict,
        "is_penalized": bool(hard_caps)
    }
