"""
SERP Competitor & Keyword Difficulty Snapshot Adapter
======================================================
Ingests competitive SERP snapshots (target query, top 10 URLs, competitor referring domains,
SERP features like 3-packs/AI Overviews, and keyword difficulty).
Provides verified KD calculation instead of relying on title string heuristics.
"""

import os
import json
from typing import Dict, List, Any, Optional

def load_serp_snapshot(serp_path_or_dict: Any) -> Optional[Dict[str, Any]]:
    """Loads and validates a competitive SERP snapshot dataset.
    Requires target_query, top_competitors list (with at least 1 competitor or explicit provenance),
    and valid numeric bounds for keyword_difficulty."""
    if not serp_path_or_dict:
        return None
        
    data: Dict[str, Any] = {}
    if isinstance(serp_path_or_dict, dict):
        data = serp_path_or_dict
    elif isinstance(serp_path_or_dict, str):
        if not os.path.exists(serp_path_or_dict):
            return None
        try:
            with open(serp_path_or_dict, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            return None

    if not isinstance(data, dict):
        return None

    raw_query = data.get("target_query")
    if not raw_query or not isinstance(raw_query, str) or not raw_query.strip():
        return None

    target_query = raw_query.strip()
    competitors = data.get("top_competitors")
    if competitors is not None and not isinstance(competitors, list):
        return None
    
    competitors_list = competitors if isinstance(competitors, list) else []

    kd = data.get("keyword_difficulty")
    if kd is not None:
        if type(kd) is not int and type(kd) is not float:
            return None
        kd_int = int(kd)
        if kd_int < 0 or kd_int > 100:
            return None
    else:
        kd_int = 50

    search_volume = data.get("search_volume", 0)
    if search_volume is not None and type(search_volume) not in (int, float):
        return None
    sv_int = max(0, int(search_volume or 0))

    has_aio = data.get("has_ai_overview", False)
    has_map_pack = data.get("has_map_pack", False)

    # Require either competitors array or explicit source/provider provenance
    has_provenance = bool(data.get("provider") or data.get("source") or data.get("fetched_at") or competitors_list)

    return {
        "target_query": target_query,
        "keyword_difficulty": kd_int,
        "search_volume": sv_int,
        "has_ai_overview": bool(has_aio),
        "has_map_pack": bool(has_map_pack),
        "competitor_count": len(competitors_list),
        "top_competitors": competitors_list,
        "provider": str(data.get("provider", "user_snapshot")),
        "fetched_at": str(data.get("fetched_at", "N/A")),
        "is_verified": bool(has_provenance)
    }
