"""
Main post generator - orchestrates content selection and AI generation.
"""

import sys
import os
from datetime import datetime
from typing import Dict, Optional, List

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.generator.gemini_client import GeminiClient
from src.generator.prompt_templates import PromptTemplates
from src.filter.content_ranker import ContentRanker
from src.filter.quality_filter import QualityFilter
from src.database.database_manager import ContentDatabase


class PostGenerator:
    """Main post generator that coordinates all components."""
    
    def __init__(self, db_path: str = "data/linkedin_posts.db"):
        """Initialize the post generator."""
        self.db = ContentDatabase(db_path)
        self.gemini_client = GeminiClient()
        self.ranker = ContentRanker()
        self.quality_filter = QualityFilter()
        self.templates = PromptTemplates()
        
    def generate_news_post(self, category: Optional[str] = None, days_back: int = 7) -> Optional[Dict]:
        """
        Generate a news-based LinkedIn post.
        
        Args:
            category: Optional category filter (AI, DevOps, Cloud, DataScience)
            days_back: How many days back to look for content
            
        Returns:
            Dictionary with post content and metadata
        """
        print("\n" + "=" * 70)
        print("GENERATING NEWS POST")
        print("=" * 70)
        
        # Connect to database
        self.db.connect()
        
        try:
            # Get recent content
            print(f"\n1. Fetching content from last {days_back} days...")
            content_items = self.db.get_recent_content(days=days_back, category=category)
            
            if not content_items:
                print("   ✗ No content available")
                return None
            
            print(f"   ✓ Found {len(content_items)} items")
            
            # Apply quality filter
            print(f"\n2. Applying quality filters...")
            filtered_items = self.quality_filter.filter_content(content_items, verbose=False)
            
            if not filtered_items:
                print("   ✗ No high-quality content passed filters")
                return None
            
            print(f"   ✓ {len(filtered_items)} items passed quality checks ({len(content_items) - len(filtered_items)} filtered out)")
            
            # Show source breakdown
            source_counts = {}
            for item in filtered_items:
                source = item['source']
                source_counts[source] = source_counts.get(source, 0) + 1
            print(f"   Sources: {', '.join([f'{k}({v})' for k, v in sorted(source_counts.items())])}")
            
            # Rank content
            print("\n3. Ranking content by score (prioritizing quality sources)...")
            top_items = self.ranker.get_top_items(filtered_items, n=10)
            
            print(f"   ✓ Top {len(top_items)} items ranked")
            
            # Show source distribution
            source_counts = {}
            for item in top_items[:5]:
                source = item['source']
                source_counts[source] = source_counts.get(source, 0) + 1
            
            print(f"   Top 5 sources: {', '.join([f'{k}({v})' for k, v in source_counts.items()])}")
            
            # Prefer ArXiv (research papers) if available in top 5
            arxiv_items = [item for item in top_items[:5] if item['source'] == 'ArXiv']
            if arxiv_items:
                best_item = arxiv_items[0]
                print(f"   ✓ Prioritizing ArXiv research paper (highest quality)")
            else:
                best_item = top_items[0]
                print(f"   ✓ Using top-ranked item")
            
            # Display top 3 for reference
            print(f"\n   Top 3 candidates:")
            for i, item in enumerate(top_items[:3], 1):
                print(f"      {i}. [{item['source']}] {item['title'][:50]}... (Score: {item['calculated_score']:.2f})")
            
            print(f"\n4. Selected: {best_item['title'][:60]}...")
            print(f"   Source: {best_item['source']} (Quality Score: {self.ranker.calculate_source_quality_score(best_item['source'])}/100)")
            print(f"   Category: {best_item['category']}")
            print(f"   Overall Score: {best_item['calculated_score']:.2f}")
            
            # Generate prompt
            print("\n5. Generating AI prompt...")
            prompt = self.templates.news_post_prompt(best_item)
            print("   ✓ Prompt created")
            
            # Generate post
            print("\n6. Generating post with Gemini AI...")
            post_content = self.gemini_client.generate_with_retry(prompt)
            
            if not post_content:
                print("   ✗ Failed to generate post")
                return None
            
            print("   ✓ Post generated successfully")
            
            # Save to database
            print("\n7. Saving to database...")
            post_data = {
                'content': post_content,
                'post_type': 'news',
                'source_content_id': best_item['id']
            }
            
            post_id = self.db.save_generated_post(post_data)
            
            # Mark content as used
            self.db.mark_content_used(best_item['id'])
            
            print(f"   ✓ Saved as draft #{post_id}")
            
            # Return complete post info
            result = {
                'id': post_id,
                'content': post_content,
                'type': 'news',
                'source_title': best_item['title'],
                'source_url': best_item['url'],
                'source_category': best_item['category'],
                'created_date': datetime.now()
            }
            
            print("\n" + "=" * 70)
            print("✓ POST GENERATION COMPLETE")
            print("=" * 70)
            
            return result
            
        finally:
            self.db.close()
    
    def generate_tip_post(self, tip_content: Optional[Dict] = None) -> Optional[Dict]:
        """
        Generate a tip-based LinkedIn post.
        
        Args:
            tip_content: Optional tip dictionary. If None, will fetch from database
            
        Returns:
            Dictionary with post content and metadata
        """
        print("\n" + "=" * 70)
        print("GENERATING TIP POST")
        print("=" * 70)
        
        # Connect to database
        self.db.connect()
        
        try:
            # Get tip content
            if not tip_content:
                print("\n1. Fetching tip from database...")
                # TODO: Implement tip retrieval from database
                print("   ⚠ Using sample tip (tip library not yet implemented)")
                tip_content = {
                    'topic': 'Code Review Best Practices',
                    'category': 'Career',
                    'tip_content': 'Always review your own code first before asking others. You\'ll catch 50% of issues yourself and make better use of reviewers\' time.'
                }
            else:
                print("\n1. Using provided tip content...")
            
            print(f"   ✓ Topic: {tip_content['topic']}")
            
            # Generate prompt
            print("\n2. Generating AI prompt...")
            prompt = self.templates.tip_post_prompt(tip_content)
            print("   ✓ Prompt created")
            
            # Generate post
            print("\n3. Generating post with Gemini AI...")
            post_content = self.gemini_client.generate_with_retry(prompt)
            
            if not post_content:
                print("   ✗ Failed to generate post")
                return None
            
            print("   ✓ Post generated successfully")
            
            # Save to database
            print("\n4. Saving to database...")
            post_data = {
                'content': post_content,
                'post_type': 'tip',
                'source_content_id': None  # Tips don't have source content
            }
            
            post_id = self.db.save_generated_post(post_data)
            print(f"   ✓ Saved as draft #{post_id}")
            
            # Return complete post info
            result = {
                'id': post_id,
                'content': post_content,
                'type': 'tip',
                'topic': tip_content['topic'],
                'category': tip_content['category'],
                'created_date': datetime.now()
            }
            
            print("\n" + "=" * 70)
            print("✓ POST GENERATION COMPLETE")
            print("=" * 70)
            
            return result
            
        finally:
            self.db.close()
    
    def preview_top_content(self, days_back: int = 7, n: int = 10):
        """
        Preview top-ranked content without generating a post.
        
        Args:
            days_back: How many days back to look
            n: Number of items to show
        """
        self.db.connect()
        
        try:
            print("\n" + "=" * 70)
            print(f"TOP {n} CONTENT ITEMS (Last {days_back} days)")
            print("=" * 70)
            
            content_items = self.db.get_recent_content(days=days_back)
            
            if not content_items:
                print("\nNo content available")
                return
            
            top_items = self.ranker.get_top_items(content_items, n=n)
            
            for i, item in enumerate(top_items, 1):
                print(f"\n{i}. {item['title']}")
                print(f"   Source: {item['source']} | Category: {item['category']}")
                print(f"   Score: {item['calculated_score']:.2f} | Engagement: {item['engagement_score']}")
                print(f"   URL: {item['url']}")
            
            print("\n" + "=" * 70)
            
        finally:
            self.db.close()


# Test the generator
if __name__ == "__main__":
    print("Testing Post Generator")
    print("=" * 70)
    
    try:
        generator = PostGenerator()
        
        # Preview top content
        generator.preview_top_content(days_back=7, n=5)
        
        # Generate a news post
        print("\n\nGenerating a test news post...")
        result = generator.generate_news_post(days_back=7)
        
        if result:
            print("\n" + "=" * 70)
            print("GENERATED POST PREVIEW")
            print("=" * 70)
            print(result['content'])
            print("=" * 70)
            print(f"\nPost ID: {result['id']}")
            print(f"Type: {result['type']}")
            print(f"Source: {result['source_title']}")
            print("=" * 70)
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
