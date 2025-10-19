"""
ArXiv API scraper for research papers.
"""

import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import List, Dict
from .base_scraper import BaseScraper
import time


class ArxivScraper(BaseScraper):
    """Scraper for ArXiv research papers."""
    
    def __init__(self):
        super().__init__('ArXiv')
        self.base_url = 'http://export.arxiv.org/api/query'
        self.rate_limit_delay = 3  # ArXiv requires 3 seconds between requests
        
    def fetch_content(self, 
                     query: str = 'AI OR ML OR "machine learning" OR "deep learning" OR "neural network" OR LLM OR "large language model" OR GPT OR "computer vision" OR NLP',
                     max_results: int = 100,
                     days_back: int = 14) -> List[Dict]:
        """
        Fetch recent papers from ArXiv.
        
        Args:
            query: Search query
            max_results: Maximum number of results
            days_back: How many days back to search
            
        Returns:
            List of normalized content items
        """
        
        # Calculate date range (timezone aware)
        from datetime import timezone
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=days_back)
        
        # Build query parameters
        params = {
            'search_query': f'all:{query}',
            'start': 0,
            'max_results': max_results,
            'sortBy': 'submittedDate',
            'sortOrder': 'descending'
        }
        
        try:
            print(f"Fetching from ArXiv... ", end='', flush=True)
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            
            # Parse XML response
            root = ET.fromstring(response.content)
            namespace = {'atom': 'http://www.w3.org/2005/Atom'}
            
            items = []
            entries = root.findall('atom:entry', namespace)
            
            for entry in entries:
                # Extract data
                title = entry.find('atom:title', namespace).text.strip()
                summary = entry.find('atom:summary', namespace).text.strip()
                published = entry.find('atom:published', namespace).text
                
                # Get primary category
                category = entry.find('atom:primary_category', namespace)
                category_text = category.get('term') if category is not None else 'AI'
                
                # Get URL
                links = entry.findall('atom:link', namespace)
                url = next((link.get('href') for link in links if link.get('type') == 'text/html'), None)
                
                # Parse date
                pub_date = datetime.fromisoformat(published.replace('Z', '+00:00'))
                
                # Only include recent papers
                if pub_date >= start_date:
                    raw_item = {
                        'title': title,
                        'url': url,
                        'summary': summary[:700],  # More detailed summary for research
                        'category': self._categorize_paper(title, summary, category_text),
                        'published_date': pub_date,
                        'engagement_score': 75  # Higher base score for research papers (more valuable)
                    }
                    
                    items.append(self.normalize_item(raw_item))
            
            print(f"✓ Found {len(items)} papers")
            time.sleep(self.rate_limit_delay)  # Respect rate limit
            return items
            
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            return []
            
    def _categorize_paper(self, title: str, summary: str, arxiv_category: str) -> str:
        """Categorize paper based on content."""
        content = (title + ' ' + summary).lower()
        
        # More comprehensive keyword categorization
        if any(word in content for word in ['devops', 'kubernetes', 'docker', 'ci/cd', 'continuous integration', 'deployment', 'infrastructure']):
            return 'DevOps'
        elif any(word in content for word in ['cloud computing', 'aws', 'azure', 'gcp', 'distributed system', 'serverless', 'microservice']):
            return 'Cloud'
        elif any(word in content for word in ['data science', 'analytics', 'visualization', 'statistical', 'data mining', 'big data']):
            return 'DataScience'
        elif any(word in content for word in ['machine learning', 'deep learning', 'neural network', 'ai', 'artificial intelligence', 'llm', 'gpt', 'computer vision', 'nlp', 'natural language', 'reinforcement learning']):
            return 'AI'
        else:
            return 'AI'  # Default for most ArXiv papers


# Test the scraper
if __name__ == "__main__":
    print("Testing ArXiv Scraper")
    print("=" * 50)
    scraper = ArxivScraper()
    results = scraper.fetch_content(max_results=10)
    
    print(f"\nSample results:")
    for i, item in enumerate(results[:3], 1):
        print(f"\n{i}. {item['title'][:60]}...")
        print(f"   Category: {item['category']}")
        print(f"   Date: {item['published_date']}")
        print(f"   URL: {item['url']}")
