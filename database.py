import sqlite3
import os
from typing import List, Dict

DB_PATH = "universities.db"

def initialize_db():
    """Initialize the SQLite database with the universities table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS universities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            country TEXT NOT NULL,
            name TEXT NOT NULL,
            website TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")

def insert_universities(country: str, universities: List[Dict[str, str]]):
    """Insert universities for a specific country into the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    for uni in universities:
        try:
            cursor.execute("""
                INSERT INTO universities (country, name, website)
                VALUES (?, ?, ?)
            """, (country, uni.get('name', ''), uni.get('website', '')))
        except Exception as e:
            print(f"Error inserting {uni.get('name', 'Unknown')}: {str(e)}")
    
    conn.commit()
    conn.close()
    print(f"Inserted {len(universities)} universities for {country}")

def clear_all_data():
    """Clear all data from the universities table (use with caution)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM universities")
    conn.commit()
    conn.close()
    print("All data cleared from universities table")

def get_country_count(country: str) -> int:
    """Get the number of universities for a specific country."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM universities WHERE country = ?", (country,))
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_total_count() -> int:
    """Get the total number of universities in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM universities")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_summary():
    """Get a summary of universities by country."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT country, COUNT(*) as count
        FROM universities
        GROUP BY country
        ORDER BY country
    """)
    results = cursor.fetchall()
    conn.close()
    return results

if __name__ == "__main__":
    initialize_db()
