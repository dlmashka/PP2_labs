"""phonebook_db.py
Database helper for PhoneBook lab.
Edit DATABASE_CONFIG to match your PostgreSQL credentials.
"""
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager

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

def create_tables():
    sql = """
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100),
        phone VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(200),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    with get_conn_cursor() as (conn, cur):
        cur.execute(sql)

def insert_contact(first_name, last_name, phone, email=None):
    sql = """
    INSERT INTO phonebook (first_name, last_name, phone, email)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (phone) DO NOTHING
    RETURNING id;
    """
    with get_conn_cursor() as (conn, cur):
        cur.execute(sql, (first_name, last_name, phone, email))
        row = cur.fetchone()
        return row['id'] if row else None

def update_contact_by_phone(phone, new_first_name=None, new_last_name=None, new_phone=None, new_email=None):
    # Build dynamic update
    fields = []
    values = []
    if new_first_name is not None:
        fields.append('first_name = %s'); values.append(new_first_name)
    if new_last_name is not None:
        fields.append('last_name = %s'); values.append(new_last_name)
    if new_phone is not None:
        fields.append('phone = %s'); values.append(new_phone)
    if new_email is not None:
        fields.append('email = %s'); values.append(new_email)
    if not fields:
        return 0
    sql = f"UPDATE phonebook SET {', '.join(fields)} WHERE phone = %s RETURNING id;"
    values.append(phone)
    with get_conn_cursor() as (conn, cur):
        cur.execute(sql, tuple(values))
        row = cur.fetchone()
        return row['id'] if row else 0

def delete_contact_by_phone(phone):
    sql = "DELETE FROM phonebook WHERE phone = %s RETURNING id;"
    with get_conn_cursor() as (conn, cur):
        cur.execute(sql, (phone,))
        row = cur.fetchone()
        return row['id'] if row else 0

def delete_contact_by_name(first_name):
    sql = "DELETE FROM phonebook WHERE first_name = %s RETURNING id;"
    with get_conn_cursor() as (conn, cur):
        cur.execute(sql, (first_name,))
        row = cur.fetchone()
        return row['id'] if row else 0

def query_contacts(filter_sql='', params=()):
    sql = "SELECT id, first_name, last_name, phone, email, created_at FROM phonebook"
    if filter_sql:
        sql += ' WHERE ' + filter_sql
    sql += ' ORDER BY first_name;'
    with get_conn_cursor() as (conn, cur):
        cur.execute(sql, params)
        return cur.fetchall()
