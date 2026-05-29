"""
Migration: add session_id column to mentors, mentees, matches.

- Assigns all existing rows to session 'default' so no data is lost.
- Drops the old per-table unique constraint on email.
- Adds a composite unique constraint (email, session_id) per table.

Supports both PostgreSQL (Supabase) and SQLite (local dev).

Usage:
  cd backend
  python scripts/migrate_add_session_id.py
"""

import os
import sys

# Allow imports from the backend package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine

DEFAULT_SESSION = 'default'


def is_postgres():
    return 'postgresql' in str(engine.url) or 'postgres' in str(engine.url)


def migrate_postgres(conn):
    print("Detected PostgreSQL — running ALTER TABLE migration...")

    stmts = [
        # mentors
        f"ALTER TABLE mentors ADD COLUMN IF NOT EXISTS session_id VARCHAR NOT NULL DEFAULT '{DEFAULT_SESSION}'",
        "CREATE INDEX IF NOT EXISTS idx_mentors_session_id ON mentors(session_id)",
        "ALTER TABLE mentors DROP CONSTRAINT IF EXISTS mentors_email_key",
        "ALTER TABLE mentors ADD CONSTRAINT uq_mentor_email_session UNIQUE (email, session_id)",

        # mentees
        f"ALTER TABLE mentees ADD COLUMN IF NOT EXISTS session_id VARCHAR NOT NULL DEFAULT '{DEFAULT_SESSION}'",
        "CREATE INDEX IF NOT EXISTS idx_mentees_session_id ON mentees(session_id)",
        "ALTER TABLE mentees DROP CONSTRAINT IF EXISTS mentees_email_key",
        "ALTER TABLE mentees ADD CONSTRAINT uq_mentee_email_session UNIQUE (email, session_id)",

        # matches
        f"ALTER TABLE matches ADD COLUMN IF NOT EXISTS session_id VARCHAR NOT NULL DEFAULT '{DEFAULT_SESSION}'",
        "CREATE INDEX IF NOT EXISTS idx_matches_session_id ON matches(session_id)",
    ]

    for stmt in stmts:
        print(f"  {stmt[:80]}...")
        conn.execute(stmt if hasattr(conn, 'exec_driver_sql') else __import__('sqlalchemy').text(stmt))

    print("PostgreSQL migration complete.")


def migrate_sqlite(conn):
    import sqlite3
    print("Detected SQLite — recreating tables with new schema...")

    raw = engine.raw_connection()
    cur = raw.cursor()

    # Check if session_id already exists on mentors
    cur.execute("PRAGMA table_info(mentors)")
    mentor_cols = [row[1] for row in cur.fetchall()]

    if 'session_id' not in mentor_cols:
        cur.execute(f"ALTER TABLE mentors ADD COLUMN session_id TEXT NOT NULL DEFAULT '{DEFAULT_SESSION}'")
        print("  Added session_id to mentors")
    else:
        print("  mentors.session_id already exists, skipping")

    cur.execute("PRAGMA table_info(mentees)")
    mentee_cols = [row[1] for row in cur.fetchall()]

    if 'session_id' not in mentee_cols:
        cur.execute(f"ALTER TABLE mentees ADD COLUMN session_id TEXT NOT NULL DEFAULT '{DEFAULT_SESSION}'")
        print("  Added session_id to mentees")
    else:
        print("  mentees.session_id already exists, skipping")

    cur.execute("PRAGMA table_info(matches)")
    match_cols = [row[1] for row in cur.fetchall()]

    if 'session_id' not in match_cols:
        cur.execute(f"ALTER TABLE matches ADD COLUMN session_id TEXT NOT NULL DEFAULT '{DEFAULT_SESSION}'")
        print("  Added session_id to matches")
    else:
        print("  matches.session_id already exists, skipping")

    raw.commit()
    raw.close()

    print("SQLite migration complete.")
    print("NOTE: SQLite cannot drop/alter unique constraints after table creation.")
    print("      For a clean local setup, run: python scripts/reset_db.py")


def main():
    from sqlalchemy import text

    with engine.connect() as conn:
        if is_postgres():
            stmts = [
                f"ALTER TABLE mentors ADD COLUMN IF NOT EXISTS session_id VARCHAR NOT NULL DEFAULT '{DEFAULT_SESSION}'",
                "CREATE INDEX IF NOT EXISTS idx_mentors_session_id ON mentors(session_id)",
                "ALTER TABLE mentors DROP CONSTRAINT IF EXISTS mentors_email_key",
                "ALTER TABLE mentors ADD CONSTRAINT uq_mentor_email_session UNIQUE (email, session_id)",

                f"ALTER TABLE mentees ADD COLUMN IF NOT EXISTS session_id VARCHAR NOT NULL DEFAULT '{DEFAULT_SESSION}'",
                "CREATE INDEX IF NOT EXISTS idx_mentees_session_id ON mentees(session_id)",
                "ALTER TABLE mentees DROP CONSTRAINT IF EXISTS mentees_email_key",
                "ALTER TABLE mentees ADD CONSTRAINT uq_mentee_email_session UNIQUE (email, session_id)",

                f"ALTER TABLE matches ADD COLUMN IF NOT EXISTS session_id VARCHAR NOT NULL DEFAULT '{DEFAULT_SESSION}'",
                "CREATE INDEX IF NOT EXISTS idx_matches_session_id ON matches(session_id)",
            ]

            print("Detected PostgreSQL — running ALTER TABLE migration...")
            for stmt in stmts:
                print(f"  Running: {stmt[:90]}...")
                conn.execute(text(stmt))

            conn.commit()
            print("\nPostgreSQL migration complete. Existing rows assigned to session 'default'.")

        else:
            migrate_sqlite(conn)


if __name__ == '__main__':
    main()
