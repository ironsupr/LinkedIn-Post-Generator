"""
Content ranking and scoring system.
"""

from datetime import datetime, timezone
from typing import List, Dict
import math


class ContentRanker:
    """Ranks and scores content items for post generation."""
    
    def __init__(self):
        """Initialize ranker with scoring weights."""
        self.weights = {
            'recency': 0.4,      # 40% weight for how recent
            'engagement': 0.3,   # 30% weight for engagement metrics
            'relevance': 0.3     # 30% weight for topic relevance
        }
        
        # Keywords for relevance scoring
        self.relevance_keywords = {
            'AI': ['ai', 'artificial intelligence', 'machine learning', 'deep learning', 
                   'neural', 'gpt', 'llm', 'transformer', 'ml', 'model'],
            'DevOps': ['devops', 'kubernetes', 'docker', 'ci/cd', 'jenkins', 'automation',
                      'deployment', 'infrastructure', 'containerization', 'pipeline'],
            'Cloud': ['cloud', 'aws', 'azure', 'gcp', 'serverless', 'microservices',
                     'distributed', 'scalability', 'kubernetes'],
            'DataScience': ['data science', 'analytics', 'visualization', 'big data',
                           'statistics', 'pandas', 'numpy', 'analysis']
        }
    
    def calculate_recency_score(self, published_date) -> float:
        """
        Calculate recency score (0-100).
        More recent = higher score.
        
        Args:
            published_date: When the content was published (datetime or string)
            
        Returns:
            Score from 0-100
        """
        if not published_date:
            return 0
        
        # Convert string to datetime if needed
        if isinstance(published_date, str):
            try:
                published_date = datetime.fromisoformat(published_date.replace('Z', '+00:00'))
            except:
                return 0
        
        # Make timezone-aware if needed
        if published_date.tzinfo is None:
            published_date = published_date.replace(tzinfo=timezone.utc)
        
        now = datetime.now(timezone.utc)
        age_hours = (now - published_date).total_seconds() / 3600
        
        # Scoring based on age
        if age_hours <= 24:       # 0-1 days
            return 100
        elif age_hours <= 48:     # 1-2 days
            return 90
        elif age_hours <= 72:     # 2-3 days
            return 80
        elif age_hours <= 96:     # 3-4 days
            return 70
        elif age_hours <= 120:    # 4-5 days
            return 60
        elif age_hours <= 144:    # 5-6 days
            return 50
        elif age_hours <= 168:    # 6-7 days
            return 40
        else:                     # > 7 days
            # Exponential decay after 7 days
            days = age_hours / 24
            return max(0, 40 * math.exp(-(days - 7) / 7))
    
    def calculate_engagement_score(self, engagement_score: int) -> float:
        """
        Calculate engagement score (0-100).
        Normalized based on typical engagement ranges.
        
        Args:
            engagement_score: Raw engagement (upvotes, likes, comments, etc.)
            
        Returns:
            Score from 0-100
        """
        if not engagement_score or engagement_score < 0:
            return 0
        
        # Logarithmic scaling for engagement
        # This prevents extremely popular items from dominating
        if engagement_score < 10:
            return engagement_score * 5  # 0-50 range
        elif engagement_score < 50:
            return 50 + (engagement_score - 10) * 1.25  # 50-100 range
        elif engagement_score < 100:
            return 75 + (engagement_score - 50) * 0.5  # 75-100 range
        else:
            # Cap at 100 but allow very high engagement
            return min(100, 90 + math.log10(engagement_score - 99) * 10)
    
    def calculate_relevance_score(self, content_item: Dict) -> float:
        """
        Calculate relevance score (0-100).
        Based on keywords and category match.
        
        Args:
            content_item: Content item dictionary
            
        Returns:
            Score from 0-100
        """
        score = 50  # Base score
        
        title = content_item.get('title', '').lower()
        summary = content_item.get('summary', '').lower()
        category = content_item.get('category', '')
        
        content_text = f"{title} {summary}"
        
        # Check for category-specific keywords
        if category in self.relevance_keywords:
            keywords = self.relevance_keywords[category]
            matches = sum(1 for keyword in keywords if keyword in content_text)
            
            # Add points for keyword matches (up to +50)
            score += min(50, matches * 10)
        
        return min(100, score)
    
    def calculate_total_score(self, content_item: Dict) -> float:
        """
        Calculate total weighted score for a content item.
        
        Args:
            content_item: Content item dictionary
            
        Returns:
            Total score (0-100)
        """
        recency_score = self.calculate_recency_score(
            content_item.get('published_date')
        )
        engagement_score = self.calculate_engagement_score(
            content_item.get('engagement_score', 0)
        )
        relevance_score = self.calculate_relevance_score(content_item)
        
        total_score = (
            recency_score * self.weights['recency'] +
            engagement_score * self.weights['engagement'] +
            relevance_score * self.weights['relevance']
        )
        
        return round(total_score, 2)
    
    def rank_content(self, content_items: List[Dict]) -> List[Dict]:
        """
        Rank a list of content items by score.
        
        Args:
            content_items: List of content item dictionaries
            
        Returns:
            Sorted list with scores added
        """
        # Calculate scores for all items
        for item in content_items:
            item['calculated_score'] = self.calculate_total_score(item)
        
        # Sort by score (highest first)
        ranked_items = sorted(
            content_items,
            key=lambda x: x['calculated_score'],
            reverse=True
        )
        
        return ranked_items
    
    def get_top_items(self, content_items: List[Dict], n: int = 5) -> List[Dict]:
        """
        Get top N ranked content items.
        
        Args:
            content_items: List of content item dictionaries
            n: Number of top items to return
            
        Returns:
            Top N items sorted by score
        """
        ranked = self.rank_content(content_items)
        return ranked[:n]


# Test the ranker
if __name__ == "__main__":
    print("Testing Content Ranker")
    print("=" * 80)
    
    from datetime import timedelta
    
    # Create sample content items
    sample_items = [
        {
            'id': 1,
            'title': 'New AI breakthrough in deep learning',
            'summary': 'Researchers develop advanced neural network architecture',
            'category': 'AI',
            'published_date': datetime.now(timezone.utc) - timedelta(hours=12),
            'engagement_score': 150
        },
        {
            'id': 2,
            'title': 'Kubernetes deployment strategies',
            'summary': 'Best practices for container orchestration',
            'category': 'DevOps',
            'published_date': datetime.now(timezone.utc) - timedelta(days=3),
            'engagement_score': 80
        },
        {
            'id': 3,
            'title': 'Cloud cost optimization tips',
            'summary': 'How to reduce AWS spending',
            'category': 'Cloud',
            'published_date': datetime.now(timezone.utc) - timedelta(days=1),
            'engagement_score': 50
        }
    ]
    
    ranker = ContentRanker()
    
    print("\nRanking content items...\n")
    ranked_items = ranker.rank_content(sample_items)
    
    for i, item in enumerate(ranked_items, 1):
        print(f"{i}. {item['title']}")
        print(f"   Category: {item['category']}")
        print(f"   Score: {item['calculated_score']:.2f}")
        print(f"   Age: {(datetime.now(timezone.utc) - item['published_date']).days} days")
        print(f"   Engagement: {item['engagement_score']}")
        print()
    
    print("=" * 80)
    print("✓ Content ranker working successfully")
