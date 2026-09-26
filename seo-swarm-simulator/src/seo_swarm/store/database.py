"""
Evidence Database & SQLite Store for SEO Swarm
===============================================
Manages run-scoped evidence persistence, immutable evaluations, execution manifests,
and automated schema migrations from v1 legacy schemas.
"""

import sqlite3
import os
import json
import tempfile
from typing import List, Dict, Any, Optional

def get_default_db_path() -> str:
    """Resolves a writable database path with fallback to user home or temp directory."""
    if os.environ.get("SEO_SWARM_DB_PATH"):
        return os.environ["SEO_SWARM_DB_PATH"]
        
    repo_data = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "data"))
    if os.path.exists(repo_data) and os.access(repo_data, os.W_OK):
        return os.path.join(repo_data, "swarm.sqlite3")
        
    user_home = os.path.expanduser("~")
    swarm_dir = os.path.join(user_home, ".seo_swarm")
    try:
        os.makedirs(swarm_dir, exist_ok=True)
        return os.path.join(swarm_dir, "swarm.sqlite3")
    except Exception:
        return os.path.join(tempfile.gettempdir(), "seo_swarm.sqlite3")

def init_db(db_path: Optional[str] = None) -> sqlite3.Connection:
    target_path = db_path or get_default_db_path()
    parent = os.path.dirname(os.path.abspath(target_path))
    if parent and not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)
        
    conn = sqlite3.connect(target_path)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA foreign_keys = ON;")
    
    with conn:
        # Schema migration check for runs table
        conn.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            run_id TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            target_url TEXT,
            profile TEXT DEFAULT 'generic',
            status TEXT DEFAULT 'running',
            raw_score REAL,
            final_score REAL,
            verdict TEXT,
            summary JSON
        );
        """)
        
        # Migrate runs table if old columns are missing
        cur = conn.cursor()
        cur.execute("PRAGMA table_info(runs);")
        runs_cols = [row[1] for row in cur.fetchall()]
        if "raw_score" not in runs_cols:
            conn.execute("ALTER TABLE runs ADD COLUMN raw_score REAL;")
        if "final_score" not in runs_cols:
            conn.execute("ALTER TABLE runs ADD COLUMN final_score REAL;")
        if "verdict" not in runs_cols:
            conn.execute("ALTER TABLE runs ADD COLUMN verdict TEXT;")
        if "summary" not in runs_cols:
            conn.execute("ALTER TABLE runs ADD COLUMN summary JSON;")
            
        # Check evidence table migration
        cur.execute("PRAGMA table_info(evidence);")
        ev_cols = [row[1] for row in cur.fetchall()]
        if not ev_cols:
            # Table does not exist, create v2 schema
            conn.execute("""
            CREATE TABLE evidence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id TEXT,
                evidence_key TEXT,
                category TEXT,
                source_file TEXT,
                line_range TEXT,
                observed_fact TEXT,
                raw_payload JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (run_id) REFERENCES runs(run_id)
            );
            """)
        elif "evidence_key" not in ev_cols:
            # Migrate legacy v1 evidence table to v2 schema with auto-increment ID
            conn.execute("""
            CREATE TABLE evidence_v2 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id TEXT,
                evidence_key TEXT,
                category TEXT,
                source_file TEXT,
                line_range TEXT,
                observed_fact TEXT,
                raw_payload JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (run_id) REFERENCES runs(run_id)
            );
            """)
            conn.execute("""
            INSERT INTO evidence_v2 (run_id, evidence_key, category, source_file, line_range, observed_fact, raw_payload, created_at)
            SELECT run_id, evidence_id, category, source_file, line_range, observed_fact, raw_payload, created_at FROM evidence;
            """)
            conn.execute("DROP TABLE evidence;")
            conn.execute("ALTER TABLE evidence_v2 RENAME TO evidence;")
            
        # Role evaluations table
        conn.execute("""
        CREATE TABLE IF NOT EXISTS role_evaluations (
            eval_id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT,
            agent_id TEXT,
            role TEXT,
            status TEXT,
            score REAL,
            verdict TEXT,
            observations JSON,
            recommendations JSON,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (run_id) REFERENCES runs(run_id)
        );
        """)
        
    return conn

def store_run(conn: sqlite3.Connection, run_id: str, target_url: str, profile: str = "generic"):
    with conn:
        conn.execute(
            "INSERT INTO runs (run_id, target_url, profile, status) VALUES (?, ?, ?, 'running')",
            (run_id, target_url, profile)
        )

def finalize_run(
    conn: sqlite3.Connection,
    run_id: str,
    raw_score: float,
    final_score: float,
    verdict: str,
    summary: Dict[str, Any]
):
    with conn:
        conn.execute(
            "UPDATE runs SET status = 'completed', raw_score = ?, final_score = ?, verdict = ?, summary = ? WHERE run_id = ?",
            (raw_score, final_score, verdict, json.dumps(summary), run_id)
        )

def store_evidence(
    conn: sqlite3.Connection,
    run_id: str,
    evidence_key: str,
    category: str, 
    source_file: str,
    line_range: str,
    fact: str,
    payload: Dict[str, Any]
):
    with conn:
        conn.execute("""
        INSERT INTO evidence (run_id, evidence_key, category, source_file, line_range, observed_fact, raw_payload)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (run_id, evidence_key, category, source_file, line_range, fact, json.dumps(payload)))

def store_evaluation(
    conn: sqlite3.Connection,
    run_id: str,
    agent_id: str,
    role: str, 
    status: str,
    score: float,
    verdict: str,
    observations: List[Dict],
    recs: List[Dict]
):
    with conn:
        conn.execute("""
        INSERT INTO role_evaluations (run_id, agent_id, role, status, score, verdict, observations, recommendations)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (run_id, agent_id, role, status, score, verdict, json.dumps(observations), json.dumps(recs)))
