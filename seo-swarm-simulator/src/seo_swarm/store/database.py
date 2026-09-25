"""
Evidence Database & SQLite Store for SEO Swarm Lite
===================================================
Manages SQLite with WAL mode and evidence indexing.
"""

import sqlite3
import os
import json
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "swarm.sqlite3")

def init_db(db_path: str = DB_PATH) -> sqlite3.Connection:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA foreign_keys = ON;")
    
    with conn:
        # Runs table
        conn.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            run_id TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            target_url TEXT,
            profile TEXT DEFAULT 'green',
            status TEXT DEFAULT 'pending',
            summary JSON
        );
        """)
        
        # Evidence table
        conn.execute("""
        CREATE TABLE IF NOT EXISTS evidence (
            evidence_id TEXT PRIMARY KEY,
            run_id TEXT,
            category TEXT,
            source_file TEXT,
            line_range TEXT,
            observed_fact TEXT,
            raw_payload JSON,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (run_id) REFERENCES runs(run_id)
        );
        """)
        
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

def store_run(conn: sqlite3.Connection, run_id: str, target_url: str, profile: str = "green"):
    with conn:
        conn.execute("INSERT INTO runs (run_id, target_url, profile, status) VALUES (?, ?, ?, 'running')",
                     (run_id, target_url, profile))

def store_evidence(conn: sqlite3.Connection, run_id: str, evidence_id: str, category: str, 
                   source_file: str, line_range: str, fact: str, payload: Dict[str, Any]):
    with conn:
        conn.execute("""
        INSERT OR REPLACE INTO evidence (evidence_id, run_id, category, source_file, line_range, observed_fact, raw_payload)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (evidence_id, run_id, category, source_file, line_range, fact, json.dumps(payload)))

def store_evaluation(conn: sqlite3.Connection, run_id: str, agent_id: str, role: str, 
                     status: str, score: float, verdict: str, observations: List[Dict], recs: List[Dict]):
    with conn:
        conn.execute("""
        INSERT INTO role_evaluations (run_id, agent_id, role, status, score, verdict, observations, recommendations)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (run_id, agent_id, role, status, score, verdict, json.dumps(observations), json.dumps(recs)))
