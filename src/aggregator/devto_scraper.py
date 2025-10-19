"""
Dev.to API scraper.
"""

import requests
from datetime import datetime, timedelta, timezone
from typing import List, Dict
from .base_scraper import BaseScraper


class DevToScraper(BaseScraper):
    """Scraper for Dev.to articles."""
    
    def __init__(self):
        super().__init__('Dev.to')
        self.base_url = 'https://dev.to/api'
        
    def fetch_content(self, tag: str = 'devops', max_results: int = 20, days_back: int = 7) -> List[Dict]:
        """Fetch recent articles from Dev.to."""
        
        try:
            print(f"Fetching from Dev.to ({tag})... ", end='', flush=True)
            
            # Fetch articles
            params = {
                'tag': tag,
                'per_page': max_results,
                'top': 7  # Top articles from last week
            }
            
            response = requests.get(f'{self.base_url}/articles', params=params, timeout=10)
            response.raise_for_status()
            articles = response.json()
            
            items = []
            # Make cutoff_date timezone-aware to match pub_date
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_back)
            
            for article in articles:
                pub_date = datetime.fromisoformat(article['published_at'].replace('Z', '+00:00'))
                
                if pub_date >= cutoff_date:
                    raw_item = {
                        'title': article['title'],
                        'url': article['url'],
                        'summary': article.get('description', '')[:500],
                        'category': 'DevOps' if tag == 'devops' else 'Cloud',
                        'published_date': pub_date,
                        'engagement_score': article.get('public_reactions_count', 0) + 
                                          article.get('comments_count', 0)
                    }
                    
                    items.append(self.normalize_item(raw_item))
                    
            print(f"✓ Found {len(items)} articles")
            return items
            
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            return []


# Test the scraper
if __name__ == "__main__":
    print("Testing Dev.to Scraper")
    print("=" * 50)
    scraper = DevToScraper()
    
    # Test with DevOps tag
    results = scraper.fetch_content(tag='devops', max_results=10)
    
    print(f"\nSample results:")
    for i, item in enumerate(results[:3], 1):
        print(f"\n{i}. {item['title'][:60]}...")
        print(f"   Category: {item['category']}")
        print(f"   Engagement: {item['engagement_score']}")
        print(f"   URL: {item['url']}")
