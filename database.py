import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "clinic.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS appointment_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                appointment_date TEXT NOT NULL,
                session TEXT NOT NULL,
                preferred_time TEXT NOT NULL,
                reason TEXT,
                status TEXT NOT NULL DEFAULT 'Pending',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def save_appointment(name, phone, appt_date, session, preferred_time, reason=""):
    with get_connection() as conn:
        cur = conn.execute("""
            INSERT INTO appointment_requests
            (name, phone, appointment_date, session, preferred_time, reason)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, phone, appt_date, session, preferred_time, reason))
        conn.commit()
        return cur.lastrowid
