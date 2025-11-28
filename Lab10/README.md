Lab 10 - PhoneBook and Snake DB integration
======================================

Files:
- phonebook_db.py  -- helper module for DB connection and table creation
- phonebook_app.py -- CLI application: insert from CSV, insert via console, update, query, delete
- sample_contacts.csv -- example CSV for import
- snake_game_db.py  -- DB helper for Snake user and user_score tables
- snake_game.py     -- simplified Snake game (pygame) integrated with DB save/load
- requirements.txt  -- Python dependencies

Setup:
1. Install dependencies:
   pip install -r requirements.txt

2. Create a PostgreSQL database and user. Note the connection params (host, port, dbname, user, password).
3. Edit the DATABASE_CONFIG dict in phonebook_db.py and snake_game_db.py to match your DB credentials.
4. Run phonebook_app.py to create tables and use CLI functions.
   python3 phonebook_app.py

5. Run snake_game.py to play the simple Snake and save/load progress.
   python3 snake_game.py

Notes:
- These scripts use psycopg2. Make sure PostgreSQL server is running.
- snake_game.py stores simple JSON-serialized state into DB. It's a template and can be extended.
