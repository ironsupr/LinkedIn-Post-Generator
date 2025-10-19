"""
Reddit API scraper using PRAW.
NOTE: Requires Reddit API credentials in .env file.
"""

from typing import List, Dict
from .base_scraper import BaseScraper
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()


class RedditScraper(BaseScraper):
    """Scraper for Reddit posts."""
    
    def __init__(self):
        super().__init__('Reddit')
        self.reddit = None
        self._initialize_reddit()
        
    def _initialize_reddit(self):
        """Initialize Reddit API client."""
        try:
            import praw
            
            client_id = os.getenv('REDDIT_CLIENT_ID')
            client_secret = os.getenv('REDDIT_CLIENT_SECRET')
            user_agent = os.getenv('REDDIT_USER_AGENT')
            
            # Check if credentials are set
            if not client_id or client_id == 'your_reddit_client_id':
                print("⚠️  Reddit API credentials not configured. Skipping Reddit scraping.")
                return
            
            self.reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent
            )
        except ImportError:
            print("⚠️  PRAW library not installed. Skipping Reddit scraping.")
        except Exception as e:
            print(f"⚠️  Reddit initialization error: {str(e)}")
        
    def fetch_content(self, 
                     subreddits: List[str] = ['MachineLearning', 'devops'],
                     limit: int = 20,
                     days_back: int = 7) -> List[Dict]:
        """Fetch top posts from subreddits."""
        
        if not self.reddit:
            print("Skipping Reddit (not configured)... ", end='', flush=True)
            print("✓ 0 posts")
            return []
        
        try:
            print(f"Fetching from Reddit... ", end='', flush=True)
            
            items = []
            cutoff_date = datetime.now() - timedelta(days=days_back)
            
            for subreddit_name in subreddits:
                subreddit = self.reddit.subreddit(subreddit_name)
                
                # Get top posts from last week
                for post in subreddit.top(time_filter='week', limit=limit):
                    pub_date = datetime.fromtimestamp(post.created_utc)
                    
                    if pub_date >= cutoff_date and not post.stickied:
                        raw_item = {
                            'title': post.title,
                            'url': post.url if not post.is_self else f"https://reddit.com{post.permalink}",
                            'summary': post.selftext[:500] if post.selftext else post.title,
                            'category': 'AI' if subreddit_name == 'MachineLearning' else 'DevOps',
                            'published_date': pub_date,
                            'engagement_score': post.score + post.num_comments
                        }
                        
                        items.append(self.normalize_item(raw_item))
                        
            print(f"✓ Found {len(items)} posts")
            return items
            
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            return []


# Test the scraper
if __name__ == "__main__":
    print("Testing Reddit Scraper")
    print("=" * 50)
    scraper = RedditScraper()
    results = scraper.fetch_content(subreddits=['MachineLearning'], limit=10)
    
    if results:
        print(f"\nSample results:")
        for i, item in enumerate(results[:3], 1):
            print(f"\n{i}. {item['title'][:60]}...")
            print(f"   Category: {item['category']}")
            print(f"   Engagement: {item['engagement_score']}")
