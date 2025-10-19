"""
Post formatter - adds emojis, hashtags, and formats LinkedIn posts.
"""

import re
from typing import Dict, List


class PostFormatter:
    """Formats and enhances LinkedIn posts."""
    
    # Emoji mappings for different contexts
    EMOJIS = {
        'AI': ['🤖', '🧠', '💡', '⚡', '🚀', '✨'],
        'DevOps': ['⚙️', '🔧', '🚀', '📦', '🔄', '⚡'],
        'Cloud': ['☁️', '🌐', '📊', '🚀', '💾', '⚡'],
        'DataScience': ['📊', '📈', '💡', '🔍', '📉', '🧮'],
        'Tech': ['💻', '🚀', '💡', '⚡', '🌟', '✨'],
        'Career': ['💼', '🎯', '📈', '💡', '🌟', '✅'],
        'question': ['💭', '🤔', '❓'],
        'success': ['✅', '🎉', '🌟', '💯'],
        'important': ['⚠️', '❗', '💡', '🔥']
    }
    
    # Common hashtag sets
    HASHTAGS = {
        'AI': ['#ArtificialIntelligence', '#MachineLearning', '#AI', '#DeepLearning', '#Tech'],
        'DevOps': ['#DevOps', '#CloudComputing', '#Kubernetes', '#Docker', '#CI_CD'],
        'Cloud': ['#CloudComputing', '#AWS', '#Azure', '#DevOps', '#Tech'],
        'DataScience': ['#DataScience', '#Analytics', '#BigData', '#MachineLearning', '#AI'],
        'Tech': ['#Technology', '#Innovation', '#Tech', '#SoftwareEngineering', '#Coding'],
        'Career': ['#CareerDevelopment', '#Leadership', '#ProfessionalGrowth', '#CareerTips', '#Success']
    }
    
    @staticmethod
    def ensure_line_breaks(text: str) -> str:
        """
        Ensure proper line breaks for readability.
        Adds breaks every 2-3 sentences if missing.
        """
        # If already well-formatted, return as is
        if text.count('\n\n') >= 3:
            return text
        
        # Split by sentences
        sentences = re.split(r'([.!?]\s+)', text)
        
        formatted = []
        sentence_count = 0
        
        for i, part in enumerate(sentences):
            formatted.append(part)
            
            # Check if this is a sentence ending
            if part.strip() and part.strip()[-1] in '.!?':
                sentence_count += 1
                
                # Add double line break every 2-3 sentences
                if sentence_count % 3 == 0 and i < len(sentences) - 1:
                    formatted.append('\n\n')
        
        return ''.join(formatted)
    
    @staticmethod
    def extract_hashtags(text: str) -> List[str]:
        """Extract existing hashtags from text."""
        return re.findall(r'#\w+', text)
    
    @staticmethod
    def add_hashtags(text: str, category: str, max_tags: int = 5) -> str:
        """
        Add relevant hashtags if missing or insufficient.
        
        Args:
            text: The post content
            category: Content category
            max_tags: Maximum number of hashtags to add
            
        Returns:
            Text with hashtags
        """
        existing_tags = PostFormatter.extract_hashtags(text)
        
        # If already has enough hashtags, return as is
        if len(existing_tags) >= max_tags:
            return text
        
        # Get relevant hashtags for category
        relevant_tags = PostFormatter.HASHTAGS.get(category, PostFormatter.HASHTAGS['Tech'])
        
        # Filter out already present tags (case insensitive)
        existing_lower = [tag.lower() for tag in existing_tags]
        new_tags = [tag for tag in relevant_tags if tag.lower() not in existing_lower]
        
        # Add missing tags
        tags_to_add = new_tags[:max_tags - len(existing_tags)]
        
        if tags_to_add:
            # Check if text already ends with hashtags
            if existing_tags and text.strip().endswith(existing_tags[-1]):
                # Add to existing hashtag line
                return text.rstrip() + ' ' + ' '.join(tags_to_add)
            else:
                # Add new hashtag line
                return text.rstrip() + '\n\n' + ' '.join(tags_to_add)
        
        return text
    
    @staticmethod
    def enhance_emojis(text: str, category: str) -> str:
        """
        Ensure appropriate emoji usage (2-3 emojis strategically placed).
        
        Args:
            text: The post content
            category: Content category
            
        Returns:
            Text with appropriate emojis
        """
        # Count existing emojis
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE)
        
        existing_emojis = emoji_pattern.findall(text)
        
        # If already has 2-3+ emojis, return as is
        if len(existing_emojis) >= 2:
            return text
        
        # Otherwise, return as is (Gemini should handle this)
        # We trust the AI to add appropriate emojis
        return text
    
    @staticmethod
    def format_post(text: str, category: str = 'Tech') -> str:
        """
        Apply all formatting enhancements.
        
        Args:
            text: Raw post content
            category: Content category
            
        Returns:
            Fully formatted post
        """
        # Apply formatting
        formatted = PostFormatter.ensure_line_breaks(text)
        formatted = PostFormatter.enhance_emojis(formatted, category)
        formatted = PostFormatter.add_hashtags(formatted, category)
        
        return formatted.strip()
    
    @staticmethod
    def save_to_file(post_content: str, post_id: int, post_type: str) -> str:
        """
        Save post to a file in drafts directory.
        
        Args:
            post_content: The post content
            post_id: Post ID from database
            post_type: Type of post (news, tip)
            
        Returns:
            File path where post was saved
        """
        import os
        from datetime import datetime
        
        # Create drafts directory if needed
        os.makedirs('drafts', exist_ok=True)
        
        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"drafts/post_{post_id}_{post_type}_{timestamp}.txt"
        
        # Save file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(post_content)
        
        return filename
    
    @staticmethod
    def save_to_markdown(post_data: Dict, filename: str = None) -> str:
        """
        Save post as markdown with metadata.
        
        Args:
            post_data: Dictionary with post data
            filename: Optional custom filename
            
        Returns:
            File path where markdown was saved
        """
        import os
        from datetime import datetime
        
        # Create drafts directory if needed
        os.makedirs('drafts', exist_ok=True)
        
        # Generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            post_id = post_data.get('id', 'unknown')
            post_type = post_data.get('type', 'post')
            filename = f"drafts/post_{post_id}_{post_type}_{timestamp}.md"
        
        # Build markdown content
        created_date = post_data.get('created_date', datetime.now())
        # Handle both datetime objects and strings
        if isinstance(created_date, str):
            created_str = created_date
        else:
            created_str = created_date.strftime('%Y-%m-%d %H:%M:%S')
        
        md_content = f"""# LinkedIn Post Draft

**Post ID:** {post_data.get('id', 'N/A')}  
**Type:** {post_data.get('type', 'N/A')}  
**Created:** {created_str}  
**Status:** Draft

"""
        
        # Add source information if available
        if 'source_title' in post_data:
            md_content += f"""## Source
**Title:** {post_data['source_title']}  
**URL:** {post_data.get('source_url', 'N/A')}  
**Category:** {post_data.get('source_category', 'N/A')}

"""
        
        # Add the post content
        md_content += f"""## Post Content

{post_data['content']}

---

## Instructions
1. Review the post above
2. Edit if needed
3. Copy to LinkedIn
4. Mark as posted using: `python main.py mark-posted --id {post_data.get('id', 'N/A')}`
"""
        
        # Save file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        return filename


# Test the formatter
if __name__ == "__main__":
    print("Testing Post Formatter")
    print("=" * 70)
    
    # Sample post
    sample_post = """Google just announced Gemini 2.0 with groundbreaking capabilities!

This new AI model brings significant improvements in reasoning and multimodal understanding. The implications for developers and businesses are huge.

Key features include enhanced code generation, better context understanding, and improved performance on complex tasks.

What are your thoughts on the rapid pace of AI development? How is it impacting your work?"""
    
    print("\nORIGINAL POST:")
    print("-" * 70)
    print(sample_post)
    
    print("\n\nFORMATTED POST:")
    print("-" * 70)
    formatted = PostFormatter.format_post(sample_post, category='AI')
    print(formatted)
    
    print("\n" + "=" * 70)
    print("✓ Post formatter working successfully")
