"""
Text summarization service using Google's Gemini API.
"""

import os
import google.generativeai as genai
from src.constants.app_constants import GEMINI_PROMPT
from src.utils.logger import Logger

class GeminiSummarizer:
    def __init__(self):
        self.logger = Logger(__name__)
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            self.logger.error("Gemini API key not found in environment variables")
            raise ValueError("Gemini API key not found")
            
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
    async def summarize(self, title: str, content: str, sources: list) -> str:
        """
        Summarize the given content using Gemini.
        
        Args:
            title (str): The title of the content
            content (str): The content to summarize
            
        Returns:
            str: Summarized content
        """
        try:
            prompt = GEMINI_PROMPT.format(title=title, content=content, sources=sources)
            response = await self.model.generate_content_async(prompt)
            
            if response.text:
                self.logger.info(f"Successfully summarized content: {title}")
                return response.text.strip()
            else:
                self.logger.warning(f"Empty response from Gemini for title: {title}")
                return content[:200] + "..."  # Fallback to truncated content
                
        except Exception as e:
            self.logger.error(f"Error summarizing content: {str(e)}")
            return content[:200] + "..."  # Fallback to truncated content 