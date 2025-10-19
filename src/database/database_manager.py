"""
Database operations and helper functions.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
import sqlite3
from .models import DatabaseManager as BaseDB


class ContentDatabase(BaseDB):
    """Extended database operations for content management."""
    
    def add_content_item(self, item: Dict) -> Optional[int]:
        """Add a new content item to database."""
        try:
            self.cursor.execute("""
                INSERT INTO content_items 
                (title, url, source, category, summary, content, 
                 keywords, engagement_score, published_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item['title'],
                item['url'],
                item['source'],
                item.get('category'),
                item.get('summary'),
                item.get('content'),
                item.get('keywords'),
                item.get('engagement_score', 0),
                item.get('published_date')
            ))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            # URL already exists
            return None
            
    def get_recent_content(self, days: int = 7, category: str = None) -> List[Dict]:
        """Get content from last N days."""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        query = """
            SELECT * FROM content_items 
            WHERE published_date >= ? 
            AND used_for_post = 0
        """
        params = [cutoff_date]
        
        if category:
            query += " AND category = ?"
            params.append(category)
            
        query += " ORDER BY engagement_score DESC, published_date DESC"
        
        self.cursor.execute(query, params)
        return [dict(row) for row in self.cursor.fetchall()]
        
    def mark_content_used(self, content_id: int):
        """Mark content as used for a post."""
        self.cursor.execute("""
            UPDATE content_items 
            SET used_for_post = 1 
            WHERE id = ?
        """, (content_id,))
        self.conn.commit()
        
    def save_generated_post(self, post: Dict) -> int:
        """Save a generated post."""
        self.cursor.execute("""
            INSERT INTO generated_posts 
            (content, post_type, source_content_id)
            VALUES (?, ?, ?)
        """, (
            post['content'],
            post['post_type'],
            post.get('source_content_id')
        ))
        self.conn.commit()
        return self.cursor.lastrowid
        
    def get_drafts(self) -> List[Dict]:
        """Get all draft posts."""
        self.cursor.execute("""
            SELECT * FROM generated_posts 
            WHERE status = 'draft'
            ORDER BY created_date DESC
        """)
        return [dict(row) for row in self.cursor.fetchall()]
        
    def get_post_by_id(self, post_id: int) -> Optional[Dict]:
        """Get a specific post by ID."""
        self.cursor.execute("""
            SELECT * FROM generated_posts 
            WHERE id = ?
        """, (post_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def get_content_by_id(self, content_id: int) -> Optional[Dict]:
        """Get a specific content item by ID."""
        self.cursor.execute("""
            SELECT * FROM content_items 
            WHERE id = ?
        """, (content_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None
        
    def mark_post_posted(self, post_id: int, engagement: Optional[int] = None):
        """Mark a post as posted."""
        self.cursor.execute("""
            UPDATE generated_posts 
            SET status = 'posted', 
                posted_date = ?,
                linkedin_engagement = ?
            WHERE id = ?
        """, (datetime.now(), engagement, post_id))
        self.conn.commit()
        
    def get_statistics(self) -> Dict:
        """Get posting statistics."""
        stats = {}
        
        # Total posts
        self.cursor.execute("SELECT COUNT(*) FROM generated_posts")
        stats['total_posts'] = self.cursor.fetchone()[0]
        
        # Posted vs drafts
        self.cursor.execute("SELECT COUNT(*) FROM generated_posts WHERE status = 'posted'")
        stats['posted_count'] = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT COUNT(*) FROM generated_posts WHERE status = 'draft'")
        stats['draft_count'] = self.cursor.fetchone()[0]
        
        # Content items in database
        self.cursor.execute("SELECT COUNT(*) FROM content_items")
        stats['total_content_items'] = self.cursor.fetchone()[0]
        
        # Last fetch date
        self.cursor.execute("SELECT MAX(fetched_date) FROM content_items")
        last_fetch = self.cursor.fetchone()[0]
        stats['last_fetch'] = last_fetch
        
        return stats
