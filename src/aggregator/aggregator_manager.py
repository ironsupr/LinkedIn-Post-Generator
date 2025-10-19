"""
Main content aggregation manager.
Coordinates all scrapers and saves content to database.
"""

from typing import List, Dict
from .arxiv_scraper import ArxivScraper
from .hackernews_scraper import HackerNewsScraper
from .devto_scraper import DevToScraper
from .reddit_scraper import RedditScraper
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.database.database_manager import ContentDatabase


class AggregatorManager:
    """Manages all content scrapers and aggregation."""
    
    def __init__(self, db_path: str = "data/linkedin_posts.db"):
        self.db = ContentDatabase(db_path)
        self.scrapers = {
            'arxiv': ArxivScraper(),
            'hackernews': HackerNewsScraper(),
            'devto': DevToScraper(),
            'reddit': RedditScraper()
        }
        
    def fetch_all_content(self, days_back: int = 7) -> Dict[str, int]:
        """Fetch content from all sources."""
        
        print("\n" + "=" * 60)
        print("FETCHING CONTENT FROM ALL SOURCES")
        print("=" * 60 + "\n")
        
        self.db.connect()
        results = {}
        
        try:
            # ArXiv
            arxiv_items = self.scrapers['arxiv'].fetch_content(days_back=days_back, max_results=30)
            results['arxiv'] = self._save_items(arxiv_items)
            
            # Hacker News
            hn_items = self.scrapers['hackernews'].fetch_content(days_back=days_back, max_results=30)
            results['hackernews'] = self._save_items(hn_items)
            
            # Dev.to (try multiple tags)
            devto_items = []
            for tag in ['devops', 'cloud']:
                items = self.scrapers['devto'].fetch_content(tag=tag, days_back=days_back, max_results=15)
                devto_items.extend(items)
            results['devto'] = self._save_items(devto_items)
            
            # Reddit
            reddit_items = self.scrapers['reddit'].fetch_content(days_back=days_back)
            results['reddit'] = self._save_items(reddit_items)
            
        finally:
            self.db.close()
            
        return results
        
    def _save_items(self, items: List[Dict]) -> int:
        """Save items to database, return count of new items."""
        saved_count = 0
        
        for item in items:
            result = self.db.add_content_item(item)
            if result is not None:
                saved_count += 1
                
        return saved_count


# Test the aggregator
if __name__ == "__main__":
    print("Testing Content Aggregator")
    print("=" * 60)
    
    manager = AggregatorManager()
    results = manager.fetch_all_content(days_back=7)
    
    print("\n" + "=" * 60)
    print("AGGREGATION SUMMARY")
    print("=" * 60)
    for source, count in results.items():
        print(f"  {source.capitalize():15s}: {count:3d} new items")
    print(f"\n  {'Total':15s}: {sum(results.values()):3d} new items")
    print("=" * 60)
