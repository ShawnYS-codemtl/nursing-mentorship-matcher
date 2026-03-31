# scripts/reset_db.py
import os
from app.database import Base, engine, init_db

# --- Import all models so they are registered with Base ---
from app.models.mentor import Mentor
from app.models.mentee import Mentee
from app.models.match import Match  # if you have a Match table

def main():
    DB_PATH = engine.url.database  # path to your SQLite file

    # --- Delete existing database file if it exists ---
    if os.path.exists(DB_PATH):
        print(f"Deleting old database at {DB_PATH}...")
        os.remove(DB_PATH)
    
    # --- Ensure folder exists ---
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    # --- Recreate database ---
    print("Recreating database tables...")
    init_db()
    print("Database reset complete.")

if __name__ == "__main__":
    main()