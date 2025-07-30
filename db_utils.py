# db_utils.py
import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("calls.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS call_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            transcript TEXT,
            summary TEXT,
            sentiment TEXT,
            action_points TEXT,
            model_used TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_call(transcript, summary, sentiment, action_points, model_used):
    conn = sqlite3.connect("calls.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO call_history (timestamp, transcript, summary, sentiment, action_points, model_used)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        transcript,
        summary,
        sentiment,
        action_points,
        model_used
    ))
    conn.commit()
    conn.close()

def get_all_calls():
    conn = sqlite3.connect("calls.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, timestamp, summary FROM call_history ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_call_by_id(call_id):
    conn = sqlite3.connect("calls.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM call_history WHERE id = ?", (call_id,))
    row = cursor.fetchone()
    conn.close()
    return row

#  NEW: Clear all call history
def clear_all_calls():
    conn = sqlite3.connect("calls.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM call_history")
    conn.commit()
    conn.close()
