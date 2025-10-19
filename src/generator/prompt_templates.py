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
        source = content_item.get('source', '')
        
        # Customize prompt based on source quality
        is_research = (source == 'ArXiv')
        content_type = "research paper" if is_research else "article"
        
        prompt = f"""You are a thought leader on LinkedIn with expertise in {category}. You translate complex technical content into valuable insights for professionals.

SOURCE CONTENT ({source}):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TITLE: {title}

SUMMARY: {summary}

URL: {url}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

YOUR MISSION:
Create a LinkedIn post that demonstrates deep understanding and provides unique value. {"This is academic research - translate complex findings into practical, actionable insights." if is_research else "Go beyond surface-level summary - provide analysis and implications."}

✨ CRITICAL QUALITY STANDARDS:

1. SUBSTANCE OVER FLUFF
   {"- Extract the key breakthrough or finding from the research" if is_research else "- Identify what's genuinely new or significant"}
   - Explain the "so what?" - real-world implications
   - Include specific details or data points (not just generalizations)
   - Avoid buzzwords like "game-changing" unless truly warranted

2. DEMONSTRATE EXPERTISE
   {"- Translate academic language into accessible insights" if is_research else "- Add your perspective or analysis"}
   - Connect to broader trends or challenges in the field
   - Mention related concepts or context that shows depth
   - Be specific about WHO this matters to and WHY

3. PROFESSIONAL WRITING STYLE
   - Hook: Start with a surprising insight, question, or bold (but accurate) statement
   - NO generic openings like "In today's digital world..."
   - Use concrete examples over abstract statements
   - Short paragraphs (2-3 sentences) with breathing room
   - Natural, conversational tone (like explaining to a smart colleague)

4. CREDIBILITY & ATTRIBUTION
   - Credit the source naturally within the post
   - {"Acknowledge it's research (adds authority)" if is_research else "Reference the publication or author if notable"}
   - Include URL at the end for those who want to dive deeper

5. ENGAGEMENT WITHOUT CLICKBAIT
   - End with a thought-provoking question (not obvious yes/no)
   - Ask about experiences, predictions, or opinions
   - Make readers want to share their perspective

📏 FORMAT (250-350 words):

[HOOK - 1-2 lines that stop the scroll]

[CONTEXT - What this is about + why you're writing about it]

[KEY INSIGHT #1 - First major takeaway with specific detail]

[KEY INSIGHT #2 - Second important point or implication]

[ANALYSIS - The "so what?" - practical implications or future outlook]

[CALL TO ACTION - Engaging question that invites genuine discussion]

[3-5 hashtags - mix of broad and niche, relevant to {category}]

🚫 AVOID:
- Generic statements that could apply to any {content_type}
- Listing features without explaining impact
- Overused phrases: "revolutionize", "game-changer" (unless truly applicable)
- Pure summary without your insights
- Excessive emojis (use 2-3 maximum, strategically)

Write a LinkedIn post that professionals will SAVE and SHARE:"""
        
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
