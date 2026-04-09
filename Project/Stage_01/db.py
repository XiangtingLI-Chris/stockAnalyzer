from __future__ import annotations
import sqlite3
import json
from typing import Optional, Any

DB_PATH = "announcement_cache.db"

def get_connect() -> sqlite3.Connection:
    connect = sqlite3.connect(DB_PATH)
    connect.row_factory = sqlite3.Row
    return connect

def init_db() -> None:
    with get_connect() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS announcement_analysis (
            url TEXT PRIMARY KEY,
            title TEXT,
            pub_time TEXT,
            content_hash TEXT,
            sentiment INTEGER,
            score REAL,
            keywords_json TEXT,
            result_json TEXT NOT NULL,
            analyzed_at TEXT NOT NULL
        )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_pub_time ON announcement_analysis(pub_time)")

def get_cached_result(url: str) -> Optional[dict[str, Any]]:
    with get_connect() as conn:
        row = conn.execute(
            "SELECT result_json FROM announcement_analysis WHERE url = ?",
            (url,)
        ).fetchone()
        if not row:
            return None
        return json.loads(row["result_json"])

def upsert_result(
        *,
        url: str,
        title: str,
        pub_time: str,
        content_hash: str,
        sentiment: int,
        score: float,
        keywords: list[str],
        result: dict[str, Any],
        analyzed_at: str
) -> None:
    with get_connect() as conn:
        conn.execute("""
        INSERT INTO announcement_analysis
            (url, title, pub_time, content_hash, sentiment, score, keywords_json, result_json, analyzed_at)
        VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(url) DO UPDATE SET
            title=excluded.title,
            pub_time=excluded.pub_time,
            content_hash=excluded.content_hash,
            sentiment=excluded.sentiment,
            score=excluded.score,
            keywords_json=excluded.keywords_json,
            result_json=excluded.result_json,
            analyzed_at=excluded.analyzed_at
        """, (
            url, title, pub_time, content_hash, sentiment, score,
            json.dumps(keywords, ensure_ascii=False),
            json.dumps(result, ensure_ascii=False),
            analyzed_at
        ))

def need_reanalyze(url: str, content_hash: str) -> bool:
    with get_connect() as conn:
        row = conn.execute(
            "SELECT content_hash FROM announcement_analysis WHERE url = ?",
            (url, )
        ).fetchone()
        if not row:
            return True
        return row["content_hash"] != content_hash
