"""
Hacker News API scraper.
"""

import requests
from datetime import datetime, timedelta, timezone
from typing import List, Dict
from .base_scraper import BaseScraper
import time


class HackerNewsScraper(BaseScraper):
    """Scraper for Hacker News top stories."""
    
    def __init__(self):
        super().__init__('HackerNews')
        self.base_url = 'https://hacker-news.firebaseio.com/v0'
        
    def fetch_content(self, max_results: int = 30, days_back: int = 7) -> List[Dict]:
        """Fetch top stories from Hacker News."""
        
        try:
            print(f"Fetching from Hacker News... ", end='', flush=True)
            
            # Get top story IDs
            response = requests.get(f'{self.base_url}/topstories.json', timeout=10)
            response.raise_for_status()
            story_ids = response.json()[:max_results]
            
            items = []
            # Make cutoff_date timezone-aware to match pub_date
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_back)
            
            for story_id in story_ids:
                # Fetch individual story
                story_response = requests.get(f'{self.base_url}/item/{story_id}.json', timeout=10)
                story = story_response.json()
                
                if not story or story.get('type') != 'story':
                    continue
                    
                # Parse timestamp (make it timezone-aware)
                pub_date = datetime.fromtimestamp(story['time'], tz=timezone.utc)
                
                # Only include recent stories
                if pub_date >= cutoff_date:
                    raw_item = {
                        'title': story.get('title', ''),
                        'url': story.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                        'summary': story.get('title', ''),  # HN doesn't have summaries
                        'category': self._categorize_story(story.get('title', '')),
                        'published_date': pub_date,
                        'engagement_score': story.get('score', 0) + story.get('descendants', 0)
                    }
                    
                    items.append(self.normalize_item(raw_item))
                    
                time.sleep(0.1)  # Be nice to the API
                
            print(f"✓ Found {len(items)} stories")
            return items
            
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            return []
            
    def _categorize_story(self, title: str) -> str:
        """Categorize story based on title."""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['ai', 'gpt', 'llm', 'machine learning', 'neural']):
            return 'AI'
        elif any(word in title_lower for word in ['devops', 'kubernetes', 'docker', 'ci/cd']):
            return 'DevOps'
        elif any(word in title_lower for word in ['cloud', 'aws', 'azure', 'serverless']):
            return 'Cloud'
        elif any(word in title_lower for word in ['data', 'analytics', 'database']):
            return 'DataScience'
        else:
            return 'Tech'


# Test the scraper
if __name__ == "__main__":
    print("Testing Hacker News Scraper")
    print("=" * 50)
    scraper = HackerNewsScraper()
    results = scraper.fetch_content(max_results=20)
    
    print(f"\nSample results:")
    for i, item in enumerate(results[:3], 1):
        print(f"\n{i}. {item['title'][:60]}...")
        print(f"   Category: {item['category']}")
        print(f"   Score: {item['engagement_score']}")
        print(f"   URL: {item['url']}")
