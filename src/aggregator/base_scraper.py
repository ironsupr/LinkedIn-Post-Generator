"""
Base scraper class for all content sources.
"""

from abc import ABC, abstractmethod
from typing import List, Dict
from datetime import datetime


class BaseScraper(ABC):
    """Abstract base class for content scrapers."""
    
    def __init__(self, source_name: str):
        self.source_name = source_name
        
    @abstractmethod
    def fetch_content(self, **kwargs) -> List[Dict]:
        """Fetch content from the source."""
        pass
        
    def normalize_item(self, raw_item: Dict) -> Dict:
        """Normalize raw item to standard format."""
        return {
            'title': raw_item.get('title', ''),
            'url': raw_item.get('url', ''),
            'source': self.source_name,
            'category': raw_item.get('category'),
            'summary': raw_item.get('summary', ''),
            'content': raw_item.get('content', ''),
            'keywords': raw_item.get('keywords', ''),
            'engagement_score': raw_item.get('engagement_score', 0),
            'published_date': raw_item.get('published_date')
        }
