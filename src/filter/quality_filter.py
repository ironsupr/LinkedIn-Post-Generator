"""
Quality filter to exclude low-quality content from LinkedIn post generation.
"""

from typing import Dict, List
import re


class QualityFilter:
    """Filter to ensure only high-quality content is used for posts."""
    
    def __init__(self):
        """Initialize quality filter with criteria."""
        # Minimum requirements by source
        self.min_title_length = {
            'ArXiv': 20,      # Research papers should have descriptive titles
            'HackerNews': 15,
            'Dev.to': 20,
            'Reddit': 25      # Reddit titles need to be more substantial
        }
        
        # Engagement thresholds (lower bar for research, higher for social)
        self.min_engagement = {
            'ArXiv': 0,       # Research papers don't need engagement
            'HackerNews': 20,
            'Dev.to': 10,
            'Reddit': 50      # Reddit posts need decent upvotes
        }
        
        # Spam/low-quality indicators
        self.spam_keywords = [
            'click here', 'buy now', 'limited offer', 'act fast',
            'amazing trick', 'you won\'t believe', 'doctors hate',
            'this one weird', 'shocking', 'must see'
        ]
        
        # Low-value Reddit subreddits (memes, low-quality discussions)
        self.excluded_subreddits = [
            'memes', 'funny', 'pics', 'aww', 'me_irl',
            'gaming', 'todayilearned', 'showerthoughts'
        ]
    
    def is_high_quality(self, content_item: Dict) -> tuple[bool, str]:
        """
        Check if content meets quality standards.
        
        Args:
            content_item: Content item to evaluate
            
        Returns:
            Tuple of (is_quality, reason) where reason explains rejection
        """
        source = content_item.get('source', '')
        title = content_item.get('title', '')
        summary = content_item.get('summary', '')
        engagement = content_item.get('engagement_score', 0)
        url = content_item.get('url', '')
        
        # Check 1: Title length
        min_length = self.min_title_length.get(source, 15)
        if len(title) < min_length:
            return False, f"Title too short ({len(title)} < {min_length})"
        
        # Check 2: Has meaningful summary
        if not summary or len(summary) < 50:
            return False, "Summary too short or missing"
        
        # Check 3: Engagement threshold (except research papers)
        if source != 'ArXiv':
            min_eng = self.min_engagement.get(source, 10)
            if engagement < min_eng:
                return False, f"Low engagement ({engagement} < {min_eng})"
        
        # Check 4: Spam/clickbait detection
        combined_text = (title + ' ' + summary).lower()
        for keyword in self.spam_keywords:
            if keyword in combined_text:
                return False, f"Spam keyword detected: '{keyword}'"
        
        # Check 5: URL quality
        if not url or not url.startswith('http'):
            return False, "Invalid or missing URL"
        
        # Check 6: Reddit-specific filters
        if source == 'Reddit':
            # Extract subreddit from URL
            subreddit_match = re.search(r'/r/([^/]+)', url)
            if subreddit_match:
                subreddit = subreddit_match.group(1).lower()
                if subreddit in self.excluded_subreddits:
                    return False, f"Excluded subreddit: r/{subreddit}"
            
            # Reddit posts should have substantial content
            if len(title) < 30 and len(summary) < 100:
                return False, "Reddit post lacks substance"
        
        # Check 7: Avoid duplicate/similar titles
        # (This would need access to existing posts - implement later)
        
        return True, "Passed all quality checks"
    
    def filter_content(self, content_items: List[Dict], verbose: bool = False) -> List[Dict]:
        """
        Filter list of content items, keeping only high quality.
        
        Args:
            content_items: List of content items
            verbose: Print filtering details
            
        Returns:
            Filtered list of high-quality items
        """
        filtered_items = []
        rejected_count = {}
        
        for item in content_items:
            is_quality, reason = self.is_high_quality(item)
            
            if is_quality:
                filtered_items.append(item)
            else:
                source = item.get('source', 'Unknown')
                rejected_count[source] = rejected_count.get(source, 0) + 1
                
                if verbose:
                    print(f"   ✗ Rejected [{source}]: {item['title'][:50]}...")
                    print(f"     Reason: {reason}")
        
        if verbose and rejected_count:
            print(f"\n   Rejected by source:")
            for source, count in rejected_count.items():
                print(f"     {source}: {count}")
        
        return filtered_items
    
    def get_quality_report(self, content_items: List[Dict]) -> Dict:
        """
        Generate quality report for content items.
        
        Args:
            content_items: List of content items
            
        Returns:
            Dictionary with quality statistics
        """
        report = {
            'total': len(content_items),
            'high_quality': 0,
            'by_source': {},
            'rejection_reasons': {}
        }
        
        for item in content_items:
            source = item.get('source', 'Unknown')
            is_quality, reason = self.is_high_quality(item)
            
            if source not in report['by_source']:
                report['by_source'][source] = {
                    'total': 0,
                    'high_quality': 0,
                    'rejected': 0
                }
            
            report['by_source'][source]['total'] += 1
            
            if is_quality:
                report['high_quality'] += 1
                report['by_source'][source]['high_quality'] += 1
            else:
                report['by_source'][source]['rejected'] += 1
                report['rejection_reasons'][reason] = report['rejection_reasons'].get(reason, 0) + 1
        
        return report


# Test the filter
if __name__ == "__main__":
    print("Testing Quality Filter")
    print("=" * 70)
    
    # Create test content items
    test_items = [
        {
            'title': 'Advanced Neural Network Architecture for Computer Vision',
            'summary': 'This paper presents a novel approach to computer vision using deep learning techniques. We demonstrate significant improvements in accuracy and efficiency over existing methods through comprehensive experiments on multiple datasets.',
            'source': 'ArXiv',
            'engagement_score': 10,
            'url': 'https://arxiv.org/abs/12345'
        },
        {
            'title': 'TIL',  # Too short
            'summary': 'Cool fact',
            'source': 'Reddit',
            'engagement_score': 100,
            'url': 'https://reddit.com/r/todayilearned/xyz'
        },
        {
            'title': 'You won\'t believe this amazing trick!',  # Clickbait
            'summary': 'Check out this amazing trick that will change your life forever!',
            'source': 'Reddit',
            'engagement_score': 200,
            'url': 'https://reddit.com/r/programming/xyz'
        },
        {
            'title': 'Kubernetes Best Practices for Production',
            'summary': 'A comprehensive guide to deploying and managing Kubernetes clusters in production environments, covering security, monitoring, and scaling strategies.',
            'source': 'Dev.to',
            'engagement_score': 45,
            'url': 'https://dev.to/article/k8s-best-practices'
        }
    ]
    
    filter = QualityFilter()
    
    print("\nTesting individual items:")
    for i, item in enumerate(test_items, 1):
        is_quality, reason = filter.is_high_quality(item)
        status = "✓ PASS" if is_quality else "✗ REJECT"
        print(f"\n{i}. {status}: {item['title'][:50]}")
        print(f"   Reason: {reason}")
    
    print("\n" + "=" * 70)
    print("Quality Report:")
    report = filter.get_quality_report(test_items)
    print(f"\nTotal items: {report['total']}")
    print(f"High quality: {report['high_quality']}")
    print(f"\nBy source:")
    for source, stats in report['by_source'].items():
        print(f"  {source}: {stats['high_quality']}/{stats['total']} passed")
    
    print("\n" + "=" * 70)
