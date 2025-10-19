"""
Database models and schema definitions.
"""

import sqlite3
from datetime import datetime
from typing import Optional, List, Dict
import os


class DatabaseManager:
    """Manages SQLite database operations."""
    
    def __init__(self, db_path: str = "data/linkedin_posts.db"):
        """Initialize database connection."""
        self.db_path = db_path
        self._ensure_db_directory()
        self.conn = None
        self.cursor = None
        
    def _ensure_db_directory(self):
        """Create data directory if it doesn't exist."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
    def connect(self):
        """Establish database connection."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Enable column access by name
        self.cursor = self.conn.cursor()
        
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            
    def create_tables(self):
        """Create all database tables."""
        
        # Content items table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS content_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                url TEXT UNIQUE NOT NULL,
                source TEXT NOT NULL,
                category TEXT,
                summary TEXT,
                content TEXT,
                keywords TEXT,
                engagement_score INTEGER DEFAULT 0,
                published_date DATETIME,
                fetched_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                used_for_post BOOLEAN DEFAULT 0
            )
        """)
        
        # Generated posts table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS generated_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                post_type TEXT,
                source_content_id INTEGER,
                created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'draft',
                posted_date DATETIME,
                linkedin_engagement INTEGER,
                FOREIGN KEY (source_content_id) REFERENCES content_items(id)
            )
        """)
        
        # Tips library table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tips_library (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                category TEXT,
                tip_content TEXT,
                used_count INTEGER DEFAULT 0,
                last_used DATETIME
            )
        """)
        
        # Configuration table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS config (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        
        self.conn.commit()
        print("✓ Database tables created successfully")


# Example usage and testing
if __name__ == "__main__":
    print("Initializing database...")
    db = DatabaseManager()
    db.connect()
    db.create_tables()
    db.close()
    print("\n✅ Database setup complete!")
    print(f"Database location: {os.path.abspath('data/linkedin_posts.db')}")
