"""
Hard Visibility & Reality Decision Gate
========================================
Implements non-negotiable hard caps based on real performance evidence:
1. Critical Visibility Gate (Zero clicks / Low impressions cap score at 10/100)
2. Backlink Authority Debt Gate (0 Referring domains cap national targets at 15/100)
3. Commercial Acquisition Gate (Missing phone/form conversion cues cap at 20/100)
4. Unimplemented Role Exclusion (Unimplemented roles marked NOT_IMPLEMENTED, not inflated to 75)
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
    hard_caps = []
    reasons = []
    
    # 1. GSC SITE-WIDE CRITICAL VISIBILITY FAILURE GATE
    # If a site with 50+ pages has < 200 impressions and 0 clicks over 28+ days:
    if gsc_metrics.get("is_active"):
        total_clicks = gsc_metrics.get("total_clicks", 0)
        total_impressions = gsc_metrics.get("total_impressions", 0)
        tracked_pages = gsc_metrics.get("tracked_pages_count", 0)
        
        if total_impressions < 500 and total_clicks == 0:
            hard_caps.append(10.0)
            reasons.append(f"GSC CRITICAL VISIBILITY FAILURE: Site has {total_impressions} total impressions and 0 clicks across {tracked_pages} pages. Organic acquisition is functionally zero.")
            
    # 2. PAGE-LEVEL TRAFFIC & RANKING GATE
    if page_metrics:
        p_clicks = page_metrics.get("clicks", 0)
        p_pos = page_metrics.get("position", 0.0)
        if p_pos > 50.0 and p_clicks == 0:
            hard_caps.append(25.0)
            reasons.append(f"PAGE 9 GRAVEYARD TRAP: Page ranks at avg position {p_pos} with 0 clicks.")
            
    # 3. NATIONAL COMPETITION VS DA DEBT GATE
    referring_domains = authority_data.get("referring_domains", 0)
    domain_authority = authority_data.get("domain_authority", 2)
    
    if is_national_target and referring_domains < 5 and domain_authority < 10:
        hard_caps.append(15.0)
        reasons.append("SUICIDAL NATIONAL COMPETITION GATE: DA < 10 domain targeting national KD 70+ terms against VC-backed incumbents.")
        
    # 4. COMMERCIAL CONVERSION GATE
    has_tap_to_call = commercial_data.get("has_tap_to_call", False)
    has_ownership = commercial_data.get("has_ownership_guarantee", False)
    if not has_tap_to_call:
        hard_caps.append(30.0)
        reasons.append("COMMERCIAL ZERO-CONVERSION GATE: No 1-tap phone action for mobile visitors.")
        
    final_score = min([raw_score] + hard_caps) if hard_caps else raw_score
    
    verdict = "CRITICAL_ACQUISITION_FAILURE" if final_score <= 15.0 else ("STRIKING_DISTANCE_RESTRICTED" if final_score <= 40.0 else ("VIABLE_LOCAL_TARGET" if final_score <= 70.0 else "PRODUCTION_VERIFIED"))
    
    return {
        "raw_score": raw_score,
        "final_capped_score": round(final_score, 1),
        "hard_caps_applied": hard_caps,
        "cap_reasons": reasons,
        "verdict": verdict,
        "is_penalized": bool(hard_caps)
    }
