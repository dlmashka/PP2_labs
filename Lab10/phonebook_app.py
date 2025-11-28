"""phonebook_app.py
Simple CLI for PhoneBook lab.
Usage: run and follow menu prompts.
"""
import csv
import json
from phonebook_db import create_tables, insert_contact, query_contacts, update_contact_by_phone, delete_contact_by_phone, delete_contact_by_name

def load_from_csv(path):
    count = 0
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            first_name = r.get('first_name') or r.get('name') or ''
            last_name = r.get('last_name') or ''
            phone = r.get('phone') or ''
            email = r.get('email') or None
            if phone and first_name:
                insert_contact(first_name.strip(), last_name.strip(), phone.strip(), email)
                count += 1
    print(f"Loaded {count} contacts from {path}")

def input_contact_console():
    first_name = input('Enter first name: ').strip()
    last_name = input('Enter last name (optional): ').strip()
    phone = input('Enter phone: ').strip()
    email = input('Enter email (optional): ').strip() or None
    inserted_id = insert_contact(first_name, last_name, phone, email)
    if inserted_id:
        print('Inserted new contact with id', inserted_id)
    else:
        print('Contact not inserted (maybe duplicate phone)')

def show_contacts():
    print('--- All contacts ---')
    rows = query_contacts()
    for r in rows:
        print(f"{r['id']}: {r['first_name']} {r['last_name']} - {r['phone']} ({r['email']})")


def search_by_name_prefix(prefix):
    rows = query_contacts('first_name ILIKE %s', (prefix + '%',))
    for r in rows:
        print(f"{r['id']}: {r['first_name']} {r['last_name']} - {r['phone']}")

def main_menu():
    create_tables()
    while True:
        print('\nPhoneBook menu:')
        print('1) Load from CSV')
        print('2) Add contact via console')
        print('3) Show all contacts')
        print('4) Search by name prefix')
        print('5) Update by phone')
        print('6) Delete by phone')
        print('7) Delete by first name')
        print('0) Exit')
        choice = input('Choose: ').strip()
        if choice == '1':
            path = input('CSV path (default sample_contacts.csv): ').strip() or 'sample_contacts.csv'
            load_from_csv(path)
        elif choice == '2':
            input_contact_console()
        elif choice == '3':
            show_contacts()
        elif choice == '4':
            prefix = input('Enter name prefix: ').strip()
            search_by_name_prefix(prefix)
        elif choice == '5':
            phone = input('Target phone to update: ').strip()
            new_first = input('New first name (leave blank to keep): ').strip() or None
            new_last = input('New last name (leave blank to keep): ').strip() or None
            new_phone = input('New phone (leave blank to keep): ').strip() or None
            new_email = input('New email (leave blank to keep): ').strip() or None
            updated = update_contact_by_phone(phone, new_first, new_last, new_phone, new_email)
            if updated:
                print('Updated contact id', updated)
            else:
                print('No contact updated (check phone)')
        elif choice == '6':
            phone = input('Phone to delete: ').strip()
            deleted = delete_contact_by_phone(phone)
            if deleted:
                print('Deleted id', deleted)
            else:
                print('No contact deleted')
        elif choice == '7':
            first_name = input('First name to delete: ').strip()
            deleted = delete_contact_by_name(first_name)
            if deleted:
                print('Deleted id', deleted)
            else:
                print('No contact deleted')
        elif choice == '0':
            break
        else:
            print('Unknown option, try again')

if __name__ == '__main__':
    main_menu()
