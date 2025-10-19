"""
Gemini AI client for generating LinkedIn posts.
"""

import google.generativeai as genai
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()


class GeminiClient:
    """Client for interacting with Google Gemini API."""
    
    def __init__(self):
        """Initialize Gemini client with API key."""
        self.api_key = os.getenv('GEMINI_API_KEY')
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Initialize the model (using gemini-2.0-flash which is free and fast)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Generation config for better control
        self.generation_config = {
            'temperature': 0.7,  # Balance creativity and consistency
            'top_p': 0.9,
            'top_k': 40,
            'max_output_tokens': 1024,
        }
        
    def generate_content(self, prompt: str) -> Optional[str]:
        """
        Generate content using Gemini API.
        
        Args:
            prompt: The prompt to send to Gemini
            
        Returns:
            Generated text or None if error
        """
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )
            
            return response.text
            
        except Exception as e:
            print(f"Error generating content: {str(e)}")
            return None
    
    def generate_with_retry(self, prompt: str, max_retries: int = 3) -> Optional[str]:
        """
        Generate content with retry logic.
        
        Args:
            prompt: The prompt to send to Gemini
            max_retries: Maximum number of retry attempts
            
        Returns:
            Generated text or None if all retries fail
        """
        for attempt in range(max_retries):
            try:
                result = self.generate_content(prompt)
                if result:
                    return result
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"Attempt {attempt + 1} failed, retrying...")
                    continue
                else:
                    print(f"All {max_retries} attempts failed: {str(e)}")
                    return None
        
        return None


# Test the client
if __name__ == "__main__":
    print("Testing Gemini Client")
    print("=" * 60)
    
    try:
        client = GeminiClient()
        print("✓ Gemini client initialized successfully")
        print(f"✓ API key configured: {client.api_key[:10]}...")
        
        # Test generation
        print("\nTesting content generation...")
        test_prompt = "Write a one-sentence professional greeting for LinkedIn."
        
        result = client.generate_content(test_prompt)
        
        if result:
            print(f"\n✓ Generation successful!")
            print(f"\nGenerated content:")
            print("-" * 60)
            print(result)
            print("-" * 60)
        else:
            print("\n✗ Generation failed")
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
