from pathlib import Path

import psycopg2

from src.config import get_env


PROJECT_ROOT = Path(__file__).resolve().parent
SCHEMA_FILE = PROJECT_ROOT / "docs" / "db_design.sql"
MOCK_DATA_FILE = PROJECT_ROOT / "docs" / "mock_data.sql"


def read_sql_file(path):
    if not path.exists():
        raise FileNotFoundError(f"SQL file not found: {path}")
    return path.read_text(encoding="utf-8")


def setup_database():
    db_url = get_env("DATABASE_URL")
    if not db_url:
        print("Error: DATABASE_URL not found in .env")
        return

    conn = None
    cursor = None

    try:
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        cursor = conn.cursor()

        print("Resetting schema school_ai...")
        cursor.execute("DROP SCHEMA IF EXISTS school_ai CASCADE;")

        print(f"Applying schema from {SCHEMA_FILE}...")
        cursor.execute(read_sql_file(SCHEMA_FILE))

        print(f"Inserting mock data from {MOCK_DATA_FILE}...")
        cursor.execute(read_sql_file(MOCK_DATA_FILE))

        print("Database setup successfully!")
        print("Sample login: PH001 / 123456")
        print("Sample email login: parentA@example.com / 123456")

    except Exception as e:
        print(f"Error during setup: {e}")
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    setup_database()
