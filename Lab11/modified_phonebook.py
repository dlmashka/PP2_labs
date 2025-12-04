#!/usr/bin/env python3
# lab11_py.py
# Python-only workflow for Lab11 (PostgreSQL + psycopg2)
# pip install psycopg2-binary

import json
import sys
import psycopg2
from psycopg2.extras import RealDictCursor


DB_CONFIG = {
    "dbname": "Lab_11_PP2",
    "user": "postgres",
    "password": "Dimash2406",
    "host": "localhost",
    "port": 5432
}

# --- DDL и PL/pgSQL объекты (исправлена add_many_users: CALL вместо PERFORM) ---
DDL_SQL = r"""
-- create table if not exists
CREATE TABLE IF NOT EXISTS PhoneBook (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  phone TEXT
);

-- search function
CREATE OR REPLACE FUNCTION search_contacts(pattern TEXT)
RETURNS TABLE(id INT, name TEXT, phone TEXT) AS $$
BEGIN
  RETURN QUERY
  SELECT id, name, phone
  FROM PhoneBook
  WHERE name ILIKE '%' || pattern || '%'
     OR phone ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;

-- add_or_update_user as PROCEDURE
CREATE OR REPLACE PROCEDURE add_or_update_user(p_name TEXT, p_phone TEXT)
LANGUAGE plpgsql AS $$
BEGIN
  IF EXISTS (SELECT 1 FROM PhoneBook WHERE name = p_name) THEN
    UPDATE PhoneBook SET phone = p_phone WHERE name = p_name;
  ELSE
    INSERT INTO PhoneBook(name, phone) VALUES (p_name, p_phone);
  END IF;
END;
$$;

-- add_many_users: loops JSON array and CALLs add_or_update_user
CREATE OR REPLACE PROCEDURE add_many_users(users_json JSON)
LANGUAGE plpgsql AS $$
DECLARE
  elem JSON;
  u_name TEXT;
  u_phone TEXT;
  invalids TEXT := '';
BEGIN
  FOR elem IN SELECT * FROM json_array_elements(users_json)
  LOOP
    u_name := elem->>'name';
    u_phone := elem->>'phone';

    -- простая валидация телефона: только цифры, минимум 5 цифр
    IF u_phone IS NOT NULL AND u_phone ~ '^\d{5,}$' THEN
      CALL add_or_update_user(u_name, u_phone); -- вызов процедуры через CALL
    ELSE
      invalids := invalids || format('(%s,%s); ', u_name, COALESCE(u_phone,'NULL'));
    END IF;
  END LOOP;

  IF invalids <> '' THEN
    RAISE NOTICE 'Incorrect entries: %', invalids;
  ELSE
    RAISE NOTICE 'All entries processed successfully.';
  END IF;
END;
$$;

-- pagination function
CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(id INT, name TEXT, phone TEXT) AS $$
BEGIN
  RETURN QUERY
  SELECT id, name, phone
  FROM PhoneBook
  ORDER BY id
  LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

-- delete_user procedure
CREATE OR REPLACE PROCEDURE delete_user(p_name TEXT DEFAULT NULL, p_phone TEXT DEFAULT NULL)
LANGUAGE plpgsql AS $$
BEGIN
  IF p_name IS NULL AND p_phone IS NULL THEN
    RAISE EXCEPTION 'Need at least name or phone to delete';
  END IF;

  DELETE FROM PhoneBook
  WHERE (p_name IS NOT NULL AND name = p_name)
     OR (p_phone IS NOT NULL AND phone = p_phone);
END;
$$;
"""

# ----------------- Helpers -----------------
def get_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print("ERROR: cannot connect to DB. Check DB_CONFIG.", file=sys.stderr)
        raise

def apply_ddl():
    print("Applying DDL (creating table/functions/procedures)...")
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(DDL_SQL)
        conn.commit()
        print("DDL applied.")
    finally:
        cur.close()
        conn.close()

def call_add_or_update_user(name, phone):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("CALL add_or_update_user(%s, %s);", (name, phone))
        conn.commit()
        print(f"CALL add_or_update_user -> ({name}, {phone})")
    finally:
        cur.close()
        conn.close()

def call_add_many_users(list_of_dicts):
    conn = get_connection()
    try:
        cur = conn.cursor()
        json_text = json.dumps(list_of_dicts, ensure_ascii=False)
        # сбросим предыдущие notices
        conn.notices.clear()
        cur.execute("CALL add_many_users(%s::json);", (json_text,))
        conn.commit()
        # печатаем notices (RAISE NOTICE попадут сюда)
        if conn.notices:
            print("Server notices:")
            for n in conn.notices:
                print("  ->", n.strip())
        else:
            print("No notices from server.")
    except Exception as e:
        print("Error while calling add_many_users:", e)
        raise
    finally:
        cur.close()
        conn.close()

def search_contacts(pattern):
    conn = get_connection()
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM search_contacts(%s);", (pattern,))
        rows = cur.fetchall()
        return rows
    finally:
        cur.close()
        conn.close()

def get_contacts_paginated(limit, offset):
    conn = get_connection()
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM get_contacts_paginated(%s, %s);", (limit, offset))
        rows = cur.fetchall()
        return rows
    finally:
        cur.close()
        conn.close()

def view_all_phonebook():
    conn = get_connection()
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM PhoneBook ORDER BY id;")
        rows = cur.fetchall()
        return rows
    finally:
        cur.close()
        conn.close()

def call_delete_user(name=None, phone=None):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("CALL delete_user(%s, %s);", (name, phone))
        conn.commit()
        print(f"CALL delete_user -> (name={name}, phone={phone})")
    finally:
        cur.close()
        conn.close()

# ----------------- Demo / example usage -----------------
def demo():
    print("=== Lab11 Python demo ===")
    apply_ddl()

    print("\n-- Add / update single users --")
    call_add_or_update_user("Ali", "77001234567")
    call_add_or_update_user("Bob", "77001230000")

    print("\n-- Batch add (one invalid phone expected) --")
    batch = [
        {"name": "Sam", "phone": "87001234"},
        {"name": "BadPhone", "phone": "abc123"},
        {"name": "Mira", "phone": "77777"}
    ]
    call_add_many_users(batch)

    print("\n-- View all rows --")
    rows = view_all_phonebook()
    for r in rows:
        print(r)

    print("\n-- Search 'Ali' --")
    print(search_contacts("Ali"))

    print("\n-- Pagination (limit=2, offset=0) --")
    print(get_contacts_paginated(2, 0))

    print("\n-- Delete Bob by name --")
    call_delete_user(name="Bob", phone=None)

    print("\n-- Final table --")
    rows = view_all_phonebook()
    for r in rows:
        print(r)

if __name__ == "__main__":
    try:
        demo()
    except Exception as exc:
        print("Unhandled error during demo:", exc, file=sys.stderr)
        sys.exit(1)
