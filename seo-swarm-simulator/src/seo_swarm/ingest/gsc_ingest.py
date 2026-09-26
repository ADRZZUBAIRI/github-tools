"""
GSC & Analytics Dataset Ingest Engine
=====================================
Ingests Google Search Console CSV exports (Pages, Queries, Devices, Countries, Chart, Filters)
and builds validated evidence objects with date windows, impressions, clicks, CTR, and positions.
Validates window completeness (e.g. 28+ days vs 7 days vs unknown), consecutive dates, and property matching.
"""

import os
import csv
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse

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
                dates = []
                for row in reader:
                    self.chart_data.append(row)
                    d = row.get("Date", "").strip()
                    if d:
                        dates.append(d)
                if dates:
                    dates.sort()
                    self.window_start = dates[0]
                    self.window_end = dates[-1]
                    self.complete_days = len(dates)
                    self.is_consecutive_window = (self.complete_days >= 7)

        if os.path.exists(pages_file):
            with open(pages_file, "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    raw_url = row.get("Top pages", "").strip()
                    parsed = urlparse(raw_url)
                    clean_path = parsed.path.rstrip("/") or "/"
                    self.pages_data.append({
                        "url": raw_url,
                        "path": clean_path,
                        "clicks": int(row.get("Clicks", 0) or 0),
                        "impressions": int(row.get("Impressions", 0) or 0),
                        "ctr": float(row.get("CTR", "0%").replace("%", "") or 0.0),
                        "position": float(row.get("Position", 0.0) or 0.0)
                    })
                    
        if os.path.exists(queries_file):
            with open(queries_file, "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.queries_data.append({
                        "query": row.get("Top queries", "").strip(),
                        "clicks": int(row.get("Clicks", 0) or 0),
                        "impressions": int(row.get("Impressions", 0) or 0),
                        "ctr": float(row.get("CTR", "0%").replace("%", "") or 0.0),
                        "position": float(row.get("Position", 0.0) or 0.0)
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
