"""
Universal Codebase & Template Discovery Adapter
================================================
Parses multiple frameworks and static markup standards:
- Static HTML (.html, .htm)
- PHP / Laravel / WordPress (.php)
- Next.js / React (.jsx, .tsx)
- Vue / Nuxt (.vue)
- Astro (.astro)
- Django / Jinja (.html templates)

Extracts clean textual representation, title metadata, headings, schemas, and public URL mappings.
"""

import os
import re
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse

def normalize_route_path(file_path: str, root_dir: str, site_url: Optional[str] = None) -> Dict[str, str]:
    """Computes clean relative route, public URL, and canonical path from a source file."""
    clean_root = root_dir.replace("\\", "/").rstrip("/")
    clean_file = file_path.replace("\\", "/")
    
    if clean_file.startswith(clean_root):
        rel_path = clean_file[len(clean_root):].lstrip("/")
    else:
        rel_path = os.path.basename(clean_file)
        
    # Remove file extension and index references for clean web route
    route = "/" + rel_path
    route = re.sub(r'/(?:index)?\.(?:html?|php|jsx?|tsx?|vue|astro)$', '', route, flags=re.IGNORECASE)
    route = re.sub(r'\.(?:html?|php|jsx?|tsx?|vue|astro)$', '', route, flags=re.IGNORECASE)
    if not route:
        route = "/"
        
    base_domain = site_url.rstrip("/") if site_url else "https://example.com"
    public_url = f"{base_domain}{route}"
    
    return {
        "rel_path": rel_path,
        "route": route,
        "public_url": public_url
    }

def extract_page_primitives(file_path: str, root_dir: Optional[str] = None, site_url: Optional[str] = None) -> Dict[str, Any]:
    """Inspects any web template or static document and normalizes into a common audit payload."""
    if not os.path.exists(file_path):
        return {
            "url": file_path,
            "route": "/" + os.path.basename(file_path),
            "public_url": f"https://example.com/{os.path.basename(file_path)}",
            "title": os.path.basename(file_path),
            "html": "",
            "text": "",
            "framework": "unknown"
        }
        
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        raw_content = f.read()

    # Determine framework / template type
    ext = os.path.splitext(file_path)[1].lower()
    framework = "static_html"
    if ext == ".php":
        framework = "php_native"
    elif ext in [".jsx", ".tsx"]:
        framework = "react_nextjs"
    elif ext == ".vue":
        framework = "vue_nuxt"
    elif ext == ".astro":
        framework = "astro"

    # Multi-pattern Title Discovery
    title = None
    # 1. Standard HTML <title>
    title_m = re.search(r'<title>([^<]+)</title>', raw_content, re.IGNORECASE)
    if title_m:
        title = title_m.group(1).strip()
    
    # 2. PHP $page_title / $title variable
    if not title:
        php_title_m = re.search(r'\$(?:page_)?title\s*=\s*["\']([^"\']+)["\']', raw_content, re.IGNORECASE)
        if php_title_m:
            title = php_title_m.group(1).strip()
            
    # 3. Next.js / React export metadata or Helmet
    if not title:
        meta_title_m = re.search(r'title:\s*["\']([^"\']+)["\']|<title>\{?["\']?([^"\'\}]+)["\']?\}?</title>', raw_content, re.IGNORECASE)
        if meta_title_m:
            title = (meta_title_m.group(1) or meta_title_m.group(2)).strip()
            
    # 4. Astro frontmatter title
    if not title:
        astro_title_m = re.search(r'---\s*[\r\n]+.*?title:\s*["\']([^"\']+)["\'].*?---', raw_content, re.DOTALL | re.IGNORECASE)
        if astro_title_m:
            title = astro_title_m.group(1).strip()
            
    # Fallback to basename
    if not title:
        title = os.path.basename(file_path)

    # Clean text extraction
    clean_text = re.sub(r'<[^>]+>', ' ', raw_content)
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()

    route_info = normalize_route_path(file_path, root_dir or os.path.dirname(file_path), site_url)

    return {
        "url": file_path,
        "rel_path": route_info["rel_path"],
        "route": route_info["route"],
        "public_url": route_info["public_url"],
        "title": title,
        "html": raw_content,
        "text": clean_text,
        "framework": framework
    }

def discover_public_codebase_routes(root_dir: str, extensions: Optional[List[str]] = None) -> List[str]:
    """Recursively crawls a codebase directory and isolates public customer routes."""
    if not extensions:
        extensions = [".html", ".htm", ".php", ".jsx", ".tsx", ".vue", ".astro"]
        
    ignored_patterns = [
        "/includes/", "/components/", "/scratch/", "/api/", "/db/", "/system/", 
        "/templates/", "/vendor/", "/node_modules/", "/.git/", "/.next/", "/dist/", "/build/", "/.cache/"
    ]
    
    public_files = []
    for root, _, files in os.walk(root_dir):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in extensions:
                full_path = os.path.join(root, f).replace("\\", "/")
                if not any(ig in full_path for ig in ignored_patterns):
                    public_files.append(full_path)
                    
    return public_files
