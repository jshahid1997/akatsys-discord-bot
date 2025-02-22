"""
Main entry point for the Discord News Bot.
"""

import os
import sys
from dotenv import load_dotenv

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.bot.news_bot import NewsBot
from src.utils.logger import Logger

def main():
    # Initialize logger
    logger = Logger(__name__)
    
    # Load environment variables
    load_dotenv()
    
    # Check required environment variables
    required_vars = [
        'DISCORD_TOKEN',
        'YOUTUBE_API_KEY',
        'NEWS_API_KEY',
        'GEMINI_API_KEY'
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        return
        
    # Initialize and run the bot
    try:
        logger.info("Starting Discord News Bot...")
        bot = NewsBot()
        bot.run(os.getenv('DISCORD_TOKEN'))
    except Exception as e:
        logger.error(f"Error running bot: {str(e)}")
        
if __name__ == "__main__":
    main() 