import psycopg2
from configparser import ConfigParser
import csv
import sys

# --- ⚙️ Функция для чтения параметров подключения (как в туториале) ---
def config(filename='database.ini', section='postgresql'):
    # Создает объект парсера
    parser = ConfigParser()
    # Читает файл
    parser.read(filename)

    # Получает секцию базы данных (postgresql)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')

    return db

# --- 🔗 Функция подключения к базе данных ---
def connect():
    conn = None
    try:
        # Чтение параметров подключения
        params = config() # Предполагается, что у вас есть файл database.ini
                          # Если нет, замените это на прямой вызов:
                          # params = {'host': 'localhost', 'database': 'YOUR_DATABASE_NAME', 'user': 'YOUR_USER', 'password': 'YOUR_PASSWORD'}

        # Подключение к PostgreSQL
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        
        # Создание курсора
        cur = conn.cursor()
        
        # Выполнение команды SQL для проверки подключения (опционально)
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(f'PostgreSQL database version: {db_version[0]}')

        # Закрытие курсора
        cur.close()

    except (Exception, psycopg2.Error) as error:
        print(f"Error while connecting to PostgreSQL: {error}")
        # Если не удалось подключиться, программа должна завершиться или продолжить работу 
        # с обработкой ошибок. Для простоты, мы можем просто выйти.
        sys.exit(1) # Выходим из программы при ошибке подключения

    return conn

# --- ➕ Функция вставки данных (способ 1: из консоли) ---
def insert_contact_console(conn):
    print("\n--- Вставка нового контакта через консоль ---")
    first_name = input("Введите имя: ")
    last_name = input("Введите фамилию (можно пропустить): ")
    phone_number = input("Введите номер телефона: ")
    
    # SQL-запрос
    sql = """INSERT INTO phonebook(first_name, last_name, phone_number)
             VALUES(%s, %s, %s) RETURNING phonebook_id;"""
    
    contact_id = None
    try:
        cur = conn.cursor()
        # Выполняем запрос с данными
        cur.execute(sql, (first_name, last_name, phone_number))
        # Получаем ID вставленной записи
        contact_id = cur.fetchone()[0]
        # Применяем изменения к базе данных
        conn.commit()
        cur.close()
        print(f"Контакт успешно добавлен с ID: {contact_id}")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Ошибка при вставке контакта: {error}")
        conn.rollback() # Откатываем транзакцию в случае ошибки

# --- ➕ Функция вставки данных (способ 2: из CSV файла) ---
def insert_contact_csv(conn, filename):
    print(f"\n--- Вставка контактов из файла: {filename} ---")
    
    # Пример формата CSV: first_name,last_name,phone_number
    # Пример данных: John,Doe,+1234567890
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            # Пропускаем заголовок, если он есть
            # next(reader) 
            
            cur = conn.cursor()
            inserted_count = 0
            
            for row in reader:
                if len(row) == 3:
                    first_name, last_name, phone_number = row
                    sql = """INSERT INTO phonebook(first_name, last_name, phone_number)
                             VALUES(%s, %s, %s) ON CONFLICT (phone_number) DO NOTHING;"""
                    # Используем ON CONFLICT DO NOTHING, чтобы игнорировать дубликаты phone_number
                    cur.execute(sql, (first_name.strip(), last_name.strip(), phone_number.strip()))
                    inserted_count += cur.rowcount
                else:
                    print(f"Предупреждение: Пропущена строка с неверным форматом: {row}")

            conn.commit()
            cur.close()
            print(f"Успешно вставлено или обновлено {inserted_count} записей.")
    except FileNotFoundError:
        print(f"Ошибка: Файл {filename} не найден.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Ошибка при загрузке из CSV: {error}")
        conn.rollback()
        
# --- ✏️ Функция обновления данных ---
def update_contact(conn):
    print("\n--- Обновление контакта ---")
    search_name = input("Введите имя или фамилию контакта для обновления: ")
    
    # Сначала ищем контакт
    sql_select = "SELECT phonebook_id, first_name, last_name, phone_number FROM phonebook WHERE first_name ILIKE %s OR last_name ILIKE %s;"
    cur = conn.cursor()
    cur.execute(sql_select, (f'%{search_name}%', f'%{search_name}%'))
    
    results = cur.fetchall()
    if not results:
        print("Контакт не найден.")
        cur.close()
        return

    print("\nНайденные контакты:")
    for i, row in enumerate(results):
        print(f"{i+1}. ID: {row[0]}, Имя: {row[1]}, Фамилия: {row[2]}, Телефон: {row[3]}")
        
    try:
        choice = int(input("Введите номер (цифру) контакта для обновления: ")) - 1
        if 0 <= choice < len(results):
            contact_id_to_update = results[choice][0]
            
            new_first_name = input(f"Введите НОВОЕ имя (Enter, чтобы оставить старое - {results[choice][1]}): ") or results[choice][1]
            new_phone = input(f"Введите НОВЫЙ телефон (Enter, чтобы оставить старый - {results[choice][3]}): ") or results[choice][3]

            # SQL-запрос на обновление
            sql_update = """UPDATE phonebook
                            SET first_name = %s, phone_number = %s
                            WHERE phonebook_id = %s;"""
                            
            cur.execute(sql_update, (new_first_name, new_phone, contact_id_to_update))
            conn.commit()
            print(f"Контакт ID {contact_id_to_update} успешно обновлен.")
        else:
            print("Неверный выбор.")
    except ValueError:
        print("Неверный ввод.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Ошибка при обновлении: {error}")
        conn.rollback()
    finally:
        cur.close()


# --- 🔍 Функция запроса данных (с разными фильтрами) ---
def select_contacts(conn):
    print("\n--- Поиск контактов ---")
    filter_type = input("Искать по [И]мени, [Ф]амилии, [Т]елефону, или [В]се контакты: ").upper()
    
    sql = "SELECT first_name, last_name, phone_number FROM phonebook "
    params = None
    
    if filter_type == 'И':
        search_term = input("Введите часть имени: ")
        sql += "WHERE first_name ILIKE %s;"
        params = (f'%{search_term}%',)
    elif filter_type == 'Ф':
        search_term = input("Введите часть фамилии: ")
        sql += "WHERE last_name ILIKE %s;"
        params = (f'%{search_term}%',)
    elif filter_type == 'Т':
        search_term = input("Введите часть номера телефона: ")
        sql += "WHERE phone_number ILIKE %s;"
        params = (f'%{search_term}%',)
    elif filter_type == 'В':
        sql += "ORDER BY first_name;"
    else:
        print("Неверный выбор фильтра.")
        return

    try:
        cur = conn.cursor()
        if params:
            cur.execute(sql, params)
        else:
            cur.execute(sql)
            
        print("\n--- Результаты поиска ---")
        for row in cur.fetchall():
            print(f"Имя: {row[0]}, Фамилия: {row[1]}, Телефон: {row[2]}")
            
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Ошибка при запросе данных: {error}")

# --- 🗑️ Функция удаления данных ---
def delete_contact(conn):
    print("\n--- Удаление контакта ---")
    delete_by = input("Удалить по [И]мени или по [Т]елефону: ").upper()
    
    sql = "DELETE FROM phonebook "
    params = None
    
    if delete_by == 'И':
        name_to_delete = input("Введите имя контакта для удаления: ")
        sql += "WHERE first_name = %s;"
        params = (name_to_delete,)
    elif delete_by == 'Т':
        phone_to_delete = input("Введите номер телефона для удаления: ")
        sql += "WHERE phone_number = %s;"
        params = (phone_to_delete,)
    else:
        print("Неверный выбор.")
        return

    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        deleted_rows = cur.rowcount
        conn.commit()
        cur.close()
        print(f"Успешно удалено {deleted_rows} записей.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Ошибка при удалении: {error}")
        conn.rollback()

# --- 🎯 Главная функция (Меню) ---
def phonebook_menu():
    conn = connect()
    if conn is None:
        print("Не удалось подключиться к базе данных. Завершение работы.")
        return

    while True:
        print("\n================================")
        print("📞 Меню Телефонной книги")
        print("================================")
        print("1. Добавить контакт (Консоль)")
        print("2. Добавить контакты (CSV файл)")
        print("3. Обновить контакт")
        print("4. Найти контакты")
        print("5. Удалить контакт")
        print("6. Выйти")
        
        choice = input("Выберите действие: ")
        
        if choice == '1':
            insert_contact_console(conn)
        elif choice == '2':
            # Создайте файл contacts.csv в той же папке!
            insert_contact_csv(conn, 'contacts.csv') 
        elif choice == '3':
            update_contact(conn)
        elif choice == '4':
            select_contacts(conn)
        elif choice == '5':
            delete_contact(conn)
        elif choice == '6':
            print("Выход из программы. До свидания!")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

    if conn:
        conn.close()

# Запуск программы
# if __name__ == '__main__':
#     # phonebook_menu() # Раскомментируйте для запуска