import sqlite3
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime

# Configuration
SQLITE_DB_PATH = "instance/database.db"
PG_CONN_URI = "postgresql+psycopg2://postgres.budszmbedmfbzhxusbzx:zRdZaT06nGNFXxqU@aws-1-eu-north-1.pooler.supabase.com:5432/postgres"

# --- Ne rien modifier sous cette ligne ---
PG_CONN_URI = PG_CONN_URI.replace("+psycopg2", "")  # psycopg2 ne reconnaît pas ce suffixe

# Connexions
print("🔗 Connexion à SQLite...")
sqlite_conn = sqlite3.connect(SQLITE_DB_PATH)     
sqlite_cur = sqlite_conn.cursor()

print("🔗 Connexion à Supabase PostgreSQL...")
pg_conn = psycopg2.connect(PG_CONN_URI)
pg_cur = pg_conn.cursor()

# === MIGRATION DES UTILISATEURS ===
print("📤 Migration de la table users...")

sqlite_cur.execute("SELECT id, username, email, password, created_at FROM users")
users = sqlite_cur.fetchall()

if users:
    execute_values(pg_cur, """
        INSERT INTO users (id, username, email, password, created_at)
        VALUES %s
        ON CONFLICT (id) DO NOTHING
    """, users)
    print(f"✅ {len(users)} utilisateurs migrés.")
else:
    print("⚠️ Aucun utilisateur trouvé.")

# === MIGRATION DES TÂCHES ===
print("\n📤 Migration de la table tasks...")

sqlite_cur.execute("SELECT id, title, description, completed, created_at, due_date, user_id FROM tasks")
tasks = sqlite_cur.fetchall()

# Conversion explicite des booléens (SQLite stocke parfois 0/1 ou texte)
converted_tasks = []
for t in tasks:
    id_, title, description, completed, created_at, due_date, user_id = t

    # Correction des dates si texte
    if isinstance(created_at, str):
        try:
            created_at = datetime.fromisoformat(created_at)
        except Exception:
            created_at = None

    if isinstance(due_date, str):
        try:
            due_date = datetime.fromisoformat(due_date)
        except Exception:
            due_date = None

    # Correction du booléen
    completed = bool(completed)

    converted_tasks.append((id_, title, description, completed, created_at, due_date, user_id))

if converted_tasks:
    execute_values(pg_cur, """
        INSERT INTO tasks (id, title, description, completed, created_at, due_date, user_id)
        VALUES %s
        ON CONFLICT (id) DO NOTHING
    """, converted_tasks)
    print(f"✅ {len(tasks)} tâches migrées.")
else:
    print("⚠️ Aucune tâche trouvée.")

# === VALIDATION ===
pg_conn.commit()
print("\n🎉 Migration terminée avec succès !")

# === FERMETURE DES CONNEXIONS ===
sqlite_conn.close()
pg_conn.close()
print("🔒 Connexions fermées proprement.")

