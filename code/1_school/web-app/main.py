import sqlite3
import os

DB_NAME = "data/database.db" # Changed to database.db for clarity for a new project

def migrate_schema():
    """
    Req 5: Database Integration - Create database schema with 3 tables
    This runs once to initialize the database structure
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Req 1: Authentication - Users table stores login credentials
    # UNIQUE constraints on username/email prevent duplicates (Req 4: Input Validation)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Req 6: Stretch Goal - Projects table enables multi-user system
    # FOREIGN KEY links to users table for data isolation
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)

    # Req 5: Database Integration (CRUD) - Words table stores vocabulary
    # FOREIGN KEYs ensure data isolation: each word belongs to a specific user & project
    # This supports Req 6: Stretch Goal - Multi-user data isolation
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            new_language_word TEXT NOT NULL,
            english_translation TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            project_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (project_id) REFERENCES projects (id)
        )
    """)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    # Ensure the database directory exists
    os.makedirs(os.path.dirname(DB_NAME), exist_ok=True)
    migrate_schema()
    print(f"Database schema migrated: {DB_NAME}")
