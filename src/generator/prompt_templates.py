"""
Prompt templates for different types of LinkedIn posts.
"""

from typing import Dict


class PromptTemplates:
    """LinkedIn post prompt templates."""
    
    @staticmethod
    def news_post_prompt(content_item: Dict) -> str:
        """
        Generate prompt for a news-based LinkedIn post.
        
        Args:
            content_item: Dictionary containing article/paper details
            
        Returns:
            Formatted prompt for Gemini
        """
        title = content_item.get('title', '')
        summary = content_item.get('summary', '')
        url = content_item.get('url', '')
        category = content_item.get('category', 'Tech')
        
        prompt = f"""You are a professional LinkedIn content creator specializing in {category} topics.

Create an engaging LinkedIn post about this recent development:

TITLE: {title}
SUMMARY: {summary}
URL: {url}
CATEGORY: {category}

REQUIREMENTS:
1. Start with a strong hook (question, surprising stat, or bold statement)
2. Keep it concise (150-250 words)
3. Use line breaks every 2-3 sentences for readability
4. Include 2-3 relevant emojis (strategic placement, not excessive)
5. Explain why this matters to professionals in {category}
6. End with an engaging question to drive comments
7. Add 3-5 relevant hashtags at the end
8. Professional yet conversational tone
9. NO promotional language
10. Focus on value and insights

STRUCTURE:
[Hook - First 1-2 lines that grab attention]

[Context - What happened/what is it]

[Analysis - Why it matters]

[Key takeaways or implications]

[Call-to-action question]

[Hashtags]

Write the complete LinkedIn post now:"""
        
        return prompt
    
    @staticmethod
    def tip_post_prompt(tip_content: Dict) -> str:
        """
        Generate prompt for a tip/advice LinkedIn post.
        
        Args:
            tip_content: Dictionary containing tip details
            
        Returns:
            Formatted prompt for Gemini
        """
        topic = tip_content.get('topic', '')
        category = tip_content.get('category', 'Career')
        tip_text = tip_content.get('tip_content', '')
        
        prompt = f"""You are a professional LinkedIn content creator sharing career and technical advice.

Create an engaging LinkedIn post sharing this professional tip:

TOPIC: {topic}
CATEGORY: {category}
TIP: {tip_text}

REQUIREMENTS:
1. Start with a relatable problem or situation
2. Keep it practical and actionable (150-250 words)
3. Use line breaks for readability
4. Include 2-3 relevant emojis
5. Share the tip as a lesson learned or best practice
6. Add specific examples or use cases
7. End with an engaging question
8. Add 3-5 relevant hashtags
9. Conversational but professional tone
10. Make it feel personal and authentic

STRUCTURE:
[Hook - Relatable problem or statement]

[Context - Why this matters]

[The Tip - Specific advice]

[How to apply it - Practical steps]

[Personal touch - Why you care about this]

[Engagement question]

[Hashtags]

Write the complete LinkedIn post now:"""
        
        return prompt
    
    @staticmethod
    def custom_post_prompt(content: str, post_type: str = "general") -> str:
        """
        Generate prompt for a custom post.
        
        Args:
            content: The content to base the post on
            post_type: Type of post (general, opinion, story, etc.)
            
        Returns:
            Formatted prompt for Gemini
        """
        prompt = f"""You are a professional LinkedIn content creator.

Create an engaging LinkedIn post based on this content:

CONTENT: {content}
TYPE: {post_type}

REQUIREMENTS:
1. Professional yet conversational tone
2. 150-250 words
3. Strong hook in first 1-2 lines
4. Line breaks every 2-3 sentences
5. 2-3 strategic emojis
6. Clear value proposition
7. Engaging question at the end
8. 3-5 relevant hashtags

Write the complete LinkedIn post now:"""
        
        return prompt
    
    @staticmethod
    def refine_post_prompt(original_post: str, feedback: str) -> str:
        """
        Generate prompt to refine an existing post.
        
        Args:
            original_post: The original LinkedIn post
            feedback: Specific feedback or changes requested
            
        Returns:
            Formatted prompt for Gemini
        """
        prompt = f"""You are a professional LinkedIn content editor.

ORIGINAL POST:
{original_post}

FEEDBACK/CHANGES REQUESTED:
{feedback}

Please refine the post based on the feedback while maintaining:
- Professional LinkedIn tone
- Proper formatting with line breaks
- Appropriate emojis (2-3)
- Engaging hook and CTA
- 3-5 hashtags

Write the refined LinkedIn post now:"""
        
        return prompt


# Test the templates
if __name__ == "__main__":
    print("Testing Prompt Templates")
    print("=" * 80)
    
    # Test news post template
    sample_content = {
        'title': 'Google Releases New AI Model Gemini 2.0',
        'summary': 'Google has announced Gemini 2.0, featuring improved reasoning capabilities and multimodal understanding.',
        'url': 'https://example.com/gemini-2',
        'category': 'AI'
    }
    
    print("\n1. NEWS POST PROMPT:")
    print("-" * 80)
    news_prompt = PromptTemplates.news_post_prompt(sample_content)
    print(news_prompt)
    
    print("\n\n2. TIP POST PROMPT:")
    print("-" * 80)
    sample_tip = {
        'topic': 'Code Review Best Practices',
        'category': 'DevOps',
        'tip_content': 'Always review your own code first before asking others to review it.'
    }
    tip_prompt = PromptTemplates.tip_post_prompt(sample_tip)
    print(tip_prompt)
    
    print("\n" + "=" * 80)
    print("✓ Prompt templates created successfully")
