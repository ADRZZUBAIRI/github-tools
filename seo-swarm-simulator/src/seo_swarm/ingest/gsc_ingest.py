import os
import csv
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse

def _extract_domain_from_url(url: str) -> str:
    raw = url.strip().lower()
    if "://" in raw:
        parsed = urlparse(raw)
        raw = parsed.netloc or parsed.path
    raw = raw.split("/")[0].split(":")[0]
    if raw.startswith("www."):
        raw = raw[4:]
    return raw

class GSCDataIngestor:
    def __init__(self, gsc_dir: Optional[str] = None, expected_site_url: Optional[str] = None):
        self.gsc_dir = gsc_dir
        self.expected_site_url = expected_site_url
        self.pages_data: List[Dict[str, Any]] = []
        self.queries_data: List[Dict[str, Any]] = []
        self.chart_data: List[Dict[str, Any]] = []
        self.countries_data: List[Dict[str, Any]] = []
        self.devices_data: List[Dict[str, Any]] = []
        self.filters_data: Dict[str, str] = {}
        
        self.window_start: Optional[str] = None
        self.window_end: Optional[str] = None
        self.complete_days: int = 0
        self.search_type: str = "Unknown"
        self.is_loaded: bool = False
        self.is_consecutive_window: bool = False
        
        if gsc_dir and os.path.exists(gsc_dir):
            self.load_from_directory(gsc_dir)

    def load_from_directory(self, gsc_dir: str):
        self.gsc_dir = gsc_dir
        pages_file = os.path.join(gsc_dir, "Pages.csv")
        queries_file = os.path.join(gsc_dir, "Queries.csv")
        chart_file = os.path.join(gsc_dir, "Chart.csv")
        filters_file = os.path.join(gsc_dir, "Filters.csv")
        countries_file = os.path.join(gsc_dir, "Countries.csv")
        devices_file = os.path.join(gsc_dir, "Devices.csv")
        
        if os.path.exists(filters_file):
            with open(filters_file, "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.reader(f)
                header = next(reader, None)
                for row in reader:
                    if len(row) >= 2:
                        self.filters_data[row[0].strip()] = row[1].strip()
            self.search_type = self.filters_data.get("Search type", "Web")

        if os.path.exists(chart_file):
            with open(chart_file, "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.DictReader(f)
                dates_set = set()
                for row in reader:
                    self.chart_data.append(row)
                    d = row.get("Date", "").strip()
                    if d:
                        try:
                            parsed_d = datetime.strptime(d, "%Y-%m-%d").date()
                            dates_set.add(parsed_d)
                        except Exception:
                            pass
                            
                if dates_set:
                    sorted_dates = sorted(list(dates_set))
                    self.window_start = str(sorted_dates[0])
                    self.window_end = str(sorted_dates[-1])
                    self.complete_days = len(sorted_dates)
                    
                    # Verify true consecutive day coverage
                    consecutive = True
                    for i in range(1, len(sorted_dates)):
                        if (sorted_dates[i] - sorted_dates[i-1]).days != 1:
                            consecutive = False
                            break
                    self.is_consecutive_window = consecutive and (self.complete_days >= 7)

        expected_host = _extract_domain_from_url(self.expected_site_url) if self.expected_site_url else None

        if os.path.exists(pages_file):
            with open(pages_file, "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    raw_url = row.get("Top pages", "").strip()
                    parsed = urlparse(raw_url)
                    page_domain = _extract_domain_from_url(raw_url)
                    
                    # If expected site host is set, reject pages from foreign domains
                    if expected_host and page_domain and page_domain != expected_host:
                        continue
                        
                    clean_path = parsed.path.rstrip("/") or "/"
                    try:
                        clicks = int(row.get("Clicks", 0) or 0)
                        impr = int(row.get("Impressions", 0) or 0)
                        ctr = float(str(row.get("CTR", "0%")).replace("%", "") or 0.0)
                        pos = float(row.get("Position", 0.0) or 0.0)
                    except Exception:
                        continue
                        
                    self.pages_data.append({
                        "url": raw_url,
                        "path": clean_path,
                        "clicks": clicks,
                        "impressions": impr,
                        "ctr": ctr,
                        "position": pos
                    })
                    
        if os.path.exists(queries_file):
            with open(queries_file, "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        q_clicks = int(row.get("Clicks", 0) or 0)
                        q_impr = int(row.get("Impressions", 0) or 0)
                        q_ctr = float(str(row.get("CTR", "0%")).replace("%", "") or 0.0)
                        q_pos = float(row.get("Position", 0.0) or 0.0)
                    except Exception:
                        continue
                    self.queries_data.append({
                        "query": row.get("Top queries", "").strip(),
                        "clicks": q_clicks,
                        "impressions": q_impr,
                        "ctr": q_ctr,
                        "position": q_pos
                    })

        if os.path.exists(countries_file):
            with open(countries_file, "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.countries_data.append(row)

        if os.path.exists(devices_file):
            with open(devices_file, "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.devices_data.append(row)
                    
        self.is_loaded = bool(self.pages_data or self.queries_data or self.chart_data)

    def get_site_metrics(self) -> Dict[str, Any]:
        if not self.is_loaded:
            return {
                "total_clicks": 0,
                "total_impressions": 0,
                "avg_ctr": 0.0,
                "avg_position": 0.0,
                "tracked_pages_count": 0,
                "window_start": None,
                "window_end": None,
                "complete_days": 0,
                "is_consecutive_window": False,
                "search_type": "Unknown",
                "is_active": False,
                "status": "NOT_LOADED"
            }
            
        total_clicks = sum(p["clicks"] for p in self.pages_data)
        total_impressions = sum(p["impressions"] for p in self.pages_data)
        avg_position = round(sum(p["position"] for p in self.pages_data) / len(self.pages_data), 1) if self.pages_data else 0.0
        avg_ctr = round((total_clicks / total_impressions * 100), 2) if total_impressions > 0 else 0.0
        
        return {
            "total_clicks": total_clicks,
            "total_impressions": total_impressions,
            "avg_ctr": avg_ctr,
            "avg_position": avg_position,
            "tracked_pages_count": len(self.pages_data),
            "window_start": self.window_start,
            "window_end": self.window_end,
            "complete_days": self.complete_days,
            "is_consecutive_window": self.is_consecutive_window,
            "search_type": self.search_type,
            "is_active": True,
            "status": "VERIFIED_LOADED"
        }

    def get_page_metrics(self, page_url_or_path: str, page_route: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Matches a target page by normalized route path or exact URL to prevent substring misattribution."""
        clean_target = page_route or urlparse(page_url_or_path).path.replace("\\", "/").rstrip("/") or "/"
        
        for p in self.pages_data:
            p_path = p.get("path", "").rstrip("/") or "/"
            p_url = p.get("url", "").rstrip("/")
            if p_path == clean_target or p_url == page_url_or_path or p_url.endswith(clean_target):
                res = dict(p)
                res["window_start"] = self.window_start
                res["window_end"] = self.window_end
                res["complete_days"] = self.complete_days
                return res
        return None
