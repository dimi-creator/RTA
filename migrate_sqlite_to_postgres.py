# Script : migrate_sqlite_to_postgres.py
import pandas as pd
from sqlalchemy import create_engine
import sqlite3
import os

# Chemin vers ta base SQLite locale
SQLITE_DB_PATH = "instance/database.db"  # adapte si besoin

# URL PostgreSQL Render (ex: postgresql://USER:PASSWORD@HOST:PORT/DBNAME)
POSTGRES_URL = os.getenv("DATABASE_URL")

# 1. Connexion à SQLite et export des tables
sqlite_conn = sqlite3.connect(SQLITE_DB_PATH)

users_df = pd.read_sql_query("SELECT * FROM users", sqlite_conn)
tasks_df = pd.read_sql_query("SELECT * FROM tasks", sqlite_conn)

sqlite_conn.close()

# 2. Connexion à PostgreSQL
pg_engine = create_engine(POSTGRES_URL)

# 3. Import des données dans PostgreSQL
# Attention : si les tables existent déjà, utilise if_exists='append'
users_df.to_sql('users', pg_engine, if_exists='append', index=False)
tasks_df.to_sql('tasks', pg_engine, if_exists='append', index=False)

print("Migration terminée avec succès !")