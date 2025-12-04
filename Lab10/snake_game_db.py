# snake_game_db.py
import psycopg2
from contextlib import contextmanager

# - DATABASE -
DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'Lab10_PP2',
    'user': 'postgres',
    'password': 'Dimash2406'
}

@contextmanager
def get_conn_cursor():
    """Контекстный менеджер для работы с базой"""
    conn = psycopg2.connect(**DATABASE_CONFIG)
    try:
        cur = conn.cursor()
        yield conn, cur
        conn.commit()
    except Exception as e:
        conn.rollback()
        print("Ошибка:", e)
        raise
    finally:
        cur.close()
        conn.close()

def create_tables():
    """Создаёт таблицы users и user_scores, если их нет"""
    sql_users = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL
    );
    """
    sql_scores = """
    CREATE TABLE IF NOT EXISTS user_scores (
        id SERIAL PRIMARY KEY,
        user_id INT REFERENCES users(id),
        score INT DEFAULT 0,
        level INT DEFAULT 1,
        saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    with get_conn_cursor() as (conn, cur):
        cur.execute(sql_users)
        cur.execute(sql_scores)
        print("Таблицы users и user_scores успешно созданы!")

if __name__ == '__main__':
    create_tables()