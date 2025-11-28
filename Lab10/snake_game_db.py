"""snake_game_db.py
DB helper for Snake user and user_score tables.
Edit DATABASE_CONFIG to your PostgreSQL server.
"""
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
import json

DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'lab10_db',
    'user': 'labuser',
    'password': 'labpass'
}

@contextmanager
def get_conn_cursor():
    conn = psycopg2.connect(**DATABASE_CONFIG)
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        yield conn, cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

def create_user_tables():
    sql = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(100) UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS user_score (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        score INTEGER,
        level INTEGER,
        saved_state JSONB,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    with get_conn_cursor() as (conn, cur):
        cur.execute(sql)

def get_or_create_user(username):
    with get_conn_cursor() as (conn, cur):
        cur.execute('SELECT id FROM users WHERE username = %s', (username,))
        row = cur.fetchone()
        if row:
            return row['id']
        cur.execute('INSERT INTO users (username) VALUES (%s) RETURNING id', (username,))
        row = cur.fetchone()
        return row['id']

def get_latest_score_for_user(user_id):
    with get_conn_cursor() as (conn, cur):
        cur.execute('SELECT score, level, saved_state FROM user_score WHERE user_id = %s ORDER BY id DESC LIMIT 1', (user_id,))
        row = cur.fetchone()
        return row

def save_user_score(user_id, score, level, saved_state_dict):
    sql = 'INSERT INTO user_score (user_id, score, level, saved_state) VALUES (%s, %s, %s, %s) RETURNING id'
    with get_conn_cursor() as (conn, cur):
        cur.execute(sql, (user_id, score, level, json.dumps(saved_state_dict)))
        row = cur.fetchone()
        return row['id'] if row else None
