"""
Text summarization service using Google's Gemini API.
"""

import os
import google.generativeai as genai
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
        
    async def summarize_batch(self, category: str, news_items: list) -> str:
        """
        Summarize a batch of news items using Gemini.
        
        Args:
            category (str): The category of news
            news_items (list): List of news items to summarize
            
        Returns:
            str: Formatted summary of important news
        """
        try:
            # Prepare the news items for the prompt
            formatted_items = []
            for item in news_items:
                formatted_items.append(
                    f"Title: {item.get('title', 'No Title')}\n"
                    f"Source: {item.get('source', 'Unknown Source')}\n"
                    f"URL: {item.get('url') or item.get('link', 'No URL')}\n"
                    f"Content: {item.get('description', 'No description available')}\n"
                )
            
            # Create the prompt
            prompt = f"""
            You are a news curator for a Discord channel focused on {category.replace('_', ' ')} news.
            Below are several news items. Please analyze them and:

            1. Filter out any items that are:
               - User queries or discussions
               - Personal opinions or blog posts
               - Duplicate or redundant information
               - Not relevant to {category.replace('_', ' ')}

            2. For the remaining important and genuine news items:
               - Provide a concise summary of each key development
               - Group related items together if they cover the same topic
               - Highlight any significant announcements or breakthroughs
               - Include relevant technical details when appropriate

            3. Format the output as follows:
               📰 **Latest {category.replace('_', ' ').title()} News Roundup**

               [For each major topic/story]:
               🔹 **[Topic/Headline]**
               [4-5 sentence summary of the key points]
               
               Sources:
               - [Source Name 1](URL1)
               - [Source Name 2](URL2)
               - ...

               [Repeat for each major topic]

            Here are the news items to analyze:

            {'-' * 80}
            {''.join(formatted_items)}
            {'-' * 80}
            """
            
            response = await self.model.generate_content_async(prompt)
            
            if response.text:
                self.logger.info(f"Successfully summarized {len(news_items)} items for category: {category}")
                return response.text.strip()
            else:
                self.logger.warning(f"Empty response from Gemini for category: {category}")
                return f"⚠️ Unable to generate summary for {category.replace('_', ' ')} news at this time."
                
        except Exception as e:
            self.logger.error(f"Error summarizing news batch: {str(e)}")
            return f"⚠️ Error processing {category.replace('_', ' ')} news: {str(e)}" 