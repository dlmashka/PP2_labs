import os
import sys
import csv
import psycopg2
from psycopg2.extras import RealDictCursor

# DB_CONFIG = {
#     "host": "localhost",
#     "port": 5432,
#     "database": "Lab_11_PP2",
#     "user": "postgres",
#     "password": "Dimash2406"
# }

# --- ГЛОБАЛЬНЫЕ ФУНКЦИИ (ОСТАВЛЯЕМ КАК ЕСТЬ) ---

def get_conn():
    # ... (ВАША ФУНКЦИЯ get_conn)
    host = input("PGHOST (default localhost): ").strip() or "localhost"
    port = input("PGPORT (default 5432): ").strip() or "5432"
    db = input("PGDATABASE (default postgres): ").strip() or "postgres"
    user = input("PGUSER (default postgres): ").strip() or "postgres"
    pwd = input("PGPASSWORD (leave empty for none): ")

    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=db,
            user=user,
            password=pwd if pwd != '' else None,
        )
        return conn
    except psycopg2.OperationalError as e:
        print("Ошибка подключения к базе данных:")
        print(" ", e)
        print("Проверьте: хост, порт, имя базы, пользователя и пароль.")
        print("Если всё верно, попробуйте снова.")
        sys.exit(1)


def create_tables(conn):
    # ... (ВАША ФУНКЦИЯ create_tables)
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS phonebook_contacts (
                    id SERIAL PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT,
                    phone TEXT UNIQUE NOT NULL,
                    email TEXT,
                    created_at TIMESTAMP DEFAULT NOW()
                );
            """)
    print("Таблица создана.")


def insert_from_csv(conn):
    # ... (ВАША ФУНКЦИЯ insert_from_csv)
    path = input("Введите путь к CSV файлу: ")

    try:
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = [(r.get('first_name'),
                     r.get('last_name'),
                     r.get('phone'),
                     r.get('email')) for r in reader]
    except:
        print("Ошибка: Не удалось открыть файл.")
        return

    with conn:
        with conn.cursor() as cur:
            cur.executemany("""
                INSERT INTO phonebook_contacts (first_name, last_name, phone, email)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (phone) DO NOTHING;
            """, data)

    print("Данные из CSV загружены.")


def insert_from_console(conn):
    # ... (ВАША ФУНКЦИЯ insert_from_console)
    fn = input("Имя: ")
    ln = input("Фамилия: ")
    phone = input("Телефон: ")
    email = input("Email: ")

    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                 INSERT INTO phonebook_contacts (first_name, last_name, phone, email)
                 VALUES (%s,%s,%s,%s)
                 ON CONFLICT (phone) DO NOTHING;
             """, (fn, ln, phone, email))

    print("Контакт добавлен.")


def update_contact(conn):
    # ... (ВАША ФУНКЦИЯ update_contact)
    print("1 — изменить имя")
    print("2 — изменить телефон")

    choice = input("Выберите: ")

    with conn:
        with conn.cursor() as cur:
            if choice == "1":
                old = input("Старое имя: ")
                new = input("Новое имя: ")
                cur.execute("UPDATE phonebook_contacts SET first_name=%s WHERE first_name=%s;", (new, old))
                print("Обновлено:", cur.rowcount)

            elif choice == "2":
                old_phone = input("Старый телефон: ")
                new_phone = input("Новый телефон: ")
                cur.execute("UPDATE phonebook_contacts SET phone=%s WHERE phone=%s;", (new_phone, old_phone))
                print("Обновлено:", cur.rowcount)


def query_contacts(conn):
    # ... (ВАША ФУНКЦИЯ query_contacts)
    print("Фильтры (enter — пропустить)")

    fn = input("Имя содержит: ")
    ln = input("Фамилия содержит: ")
    phone = input("Телефон содержит: ")
    email = input("Email содержит: ")

    clauses = []
    params = []

    if fn:
        clauses.append("first_name ILIKE %s")
        params.append(f"%{fn}%")

    if ln:
        clauses.append("last_name ILIKE %s")
        params.append(f"%{ln}%")

    if phone:
        clauses.append("phone ILIKE %s")
        params.append(f"%{phone}%")

    if email:
        clauses.append("email ILIKE %s")
        params.append(f"%{email}%")

    sql = "SELECT * FROM phonebook_contacts"
    if clauses:
        sql += " WHERE " + " AND ".join(clauses)

    sql += " ORDER BY first_name LIMIT 100;"

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql, params)
        rows = cur.fetchall()

        for r in rows:
            print(r)


def delete_contact(conn):
    # ... (ВАША ФУНКЦИЯ delete_contact)
    print("1 — удалить по имени")
    print("2 — удалить по телефону")

    choice = input("Выберите: ")

    with conn:
        with conn.cursor() as cur:
            if choice == "1":
                name = input("Имя: ")
                cur.execute("DELETE FROM phonebook_contacts WHERE first_name=%s;", (name,))
                print("Удалено:", cur.rowcount)

            else:
                phone = input("Телефон: ")
                cur.execute("DELETE FROM phonebook_contacts WHERE phone=%s;", (phone,))
                print("Удалено:", cur.rowcount)


# --- НОВЫЕ ФУНКЦИИ ДЛЯ ЛАБ 11 ---

def call_search_by_pattern(conn):
    """Вызывает функцию search_contacts_by_pattern (Задание 1)"""
    pattern = input("Введите шаблон для поиска (имя, телефон, email): ")
    
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        # Вызов SQL-функции
        cur.execute("SELECT * FROM search_contacts_by_pattern(%s);", (pattern,))
        rows = cur.fetchall()

    if rows:
        print(f"Найдено {len(rows)} совпадений:")
        for r in rows:
            print(f"  ID: {r['id']}, Имя: {r['first_name']} {r['last_name'] or ''}, Тел: {r['phone']}")
    else:
        print("Совпадений не найдено.")


def call_insert_or_update(conn):
    """Вызывает процедуру insert_or_update_contact (Задание 2)"""
    fn = input("Имя: ")
    ln = input("Фамилия (если нет, оставьте пустым): ") or None
    phone = input("Телефон: ")
    
    try:
        with conn:
            with conn.cursor() as cur:
                # Вызов SQL-процедуры
                cur.execute("CALL insert_or_update_contact(%s, %s, %s);", (fn, ln, phone))
        print(f"Контакт {fn} {ln or ''} обработан (добавлен или обновлен).")
    except psycopg2.Error as e:
        print(f"Ошибка при обработке контакта: {e.pgerror}")


def call_bulk_insert(conn):
    """Вызывает функцию bulk_insert_contacts (Задание 3)"""
    print("Вводите контакты по очереди (Имя, Телефон). Введите 'END' для завершения.")
    data_list = []
    
    while True:
        name = input("Введите Имя (или 'END'): ").strip()
        if name.upper() == 'END':
            break
        phone = input(f"Введите Телефон для {name}: ").strip()
        data_list.append(name)
        data_list.append(phone)
        
    if not data_list:
        print("Список пуст.")
        return

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        # Вызов SQL-функции с массивом в качестве аргумента
        cur.execute("SELECT * FROM bulk_insert_contacts(%s);", (data_list,))
        invalid_rows = cur.fetchall()
        
    if invalid_rows:
        print("\n!!! Обнаружены НЕКОРРЕКТНЫЕ данные (не вставлены) !!!")
        for r in invalid_rows:
            print(f"  Имя: {r['name_out']}, Тел: {r['phone_out']}, Причина: {r['reason']}")
    else:
        print("\nВсе данные в списке были успешно обработаны.")


def call_pagination_query(conn):
    """Вызывает функцию get_contacts_with_pagination (Задание 4)"""
    try:
        limit = int(input("Введите LIMIT (сколько записей показать): "))
        offset = int(input("Введите OFFSET (с какой записи начать): "))
    except ValueError:
        print("Ошибка: LIMIT и OFFSET должны быть числами.")
        return

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        # Вызов SQL-функции
        cur.execute("SELECT * FROM get_contacts_with_pagination(%s, %s);", (limit, offset))
        rows = cur.fetchall()

    if rows:
        print(f"Показаны контакты (LIMIT {limit}, OFFSET {offset}):")
        for r in rows:
            print(f"  ID: {r['id']}, Имя: {r['first_name']} {r['last_name'] or ''}, Тел: {r['phone']}")
    else:
        print("На этой странице нет записей.")


def call_delete_by_identifier(conn):
    """Вызывает процедуру delete_contact_by_identifier (Задание 5)"""
    print("Выберите способ удаления:")
    print("1 — по Имени (удалит все совпадения)")
    print("2 — по Телефону (удалит точное совпадение)")
    
    choice = input("Ваш выбор: ")
    name_param = None
    phone_param = None
    
    if choice == '1':
        name_param = input("Введите Имя для удаления: ")
    elif choice == '2':
        phone_param = input("Введите Телефон для удаления: ")
    else:
        print("Неверный выбор.")
        return
        
    with conn.cursor() as cur:
        # Вызов SQL-процедуры. OUT-параметр передаем как NULL
        cur.execute("CALL delete_contact_by_identifier(%s, %s, NULL);", (name_param, phone_param))
        
        # Получаем значение OUT-параметра rows_deleted
        # Примечание: Это работает для PostgreSQL
        cur.execute("SELECT rows_deleted;")
        rows_deleted = cur.fetchone()[0]

    print(f"Удалено записей: {rows_deleted}")


# --- ОБНОВЛЕННАЯ ФУНКЦИЯ MAIN ---

def main():
    conn = get_conn()

    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1 — создать таблицу")
        print("2 — загрузить CSV")
        print("3 — добавить контакт вручную")
        print("4 — обновить контакт")
        print("5 — найти контакты (старая реализация)")
        print("6 — удалить контакт (старая реализация)")
        print("--- LAB 11 (Procedures & Functions) ---")
        print("7 — Выполнить поиск по образцу (Функция 1)")
        print("8 — Добавить/Обновить один контакт (Процедура 2)")
        print("9 — Множественная вставка с проверкой (Функция 3)")
        print("A — Постраничный вывод (Функция 4)")
        print("B — Удалить контакт (Процедура 5)")
        print("0 — выход")

        choice = input("Выберите действие: ").upper()

        try:
            if choice == "1":
                create_tables(conn)
            elif choice == "2":
                insert_from_csv(conn)
            elif choice == "3":
                insert_from_console(conn)
            elif choice == "4":
                update_contact(conn)
            elif choice == "5":
                query_contacts(conn)
            elif choice == "6":
                delete_contact(conn)
            # НОВЫЕ ПУНКТЫ
            elif choice == "7":
                call_search_by_pattern(conn)
            elif choice == "8":
                call_insert_or_update(conn)
            elif choice == "9":
                call_bulk_insert(conn)
            elif choice == "A":
                call_pagination_query(conn)
            elif choice == "B":
                call_delete_by_identifier(conn)
            # КОНЕЦ НОВЫХ ПУНКТОВ
            elif choice == "0":
                print("Выход.")
                break
            else:
                print("Неверный выбор.")
        except psycopg2.Error as e:
            print("\n!!! ОШИБКА БАЗЫ ДАННЫХ !!!")
            print("Код ошибки:", e.pgcode)
            print("Сообщение:", e.pgerror)
            print("Убедитесь, что вы создали все процедуры/функции в базе.")
            conn.rollback() # Откат, если произошла ошибка
            
    conn.close()


if __name__ == "__main__":
    main()