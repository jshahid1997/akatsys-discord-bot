"""
Main entry point for the Discord News Bot.
"""

import os
import sys
import asyncio
import threading
from aiohttp import web
from dotenv import load_dotenv

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.bot.news_bot import NewsBot
from src.utils.logger import Logger

# Global variables
bot = None
logger = None

async def health_check(request):
    """Health check endpoint for the API."""
    return web.Response(text="OK", status=200)

async def trigger_rss(request):
    """API endpoint to trigger RSS feed check."""
    global bot, logger
    
    if not bot:
        return web.Response(text="Bot not initialized", status=500)
    
    try:
        data = await request.json()
        category = data.get('category', None)
        
        # Validate category if provided
        if category and category not in ['ai_news', 'hackathon_news', 'tech_news', 'startup_news']:
            return web.Response(text=f"Invalid category: {category}", status=400)
        
        # Get the first text channel to use for context
        channel = None
        for guild in bot.guilds:
            for ch in guild.text_channels:
                channel = ch
                break
            if channel:
                break
                
        if not channel:
            return web.Response(text="No text channel available", status=500)
            
        # Create a mock context
        class MockContext:
            async def send(self, message):
                logger.info(f"API trigger message: {message}")
                
        ctx = MockContext()
        
        # Trigger the RSS check
        await bot.manual_rss_check(ctx, category)
        
        return web.Response(
            text=f"RSS feed check triggered successfully{f' for category: {category}' if category else ''}",
            status=200
        )
    except Exception as e:
        logger.error(f"Error in trigger_rss API: {str(e)}")
        return web.Response(text=f"Error: {str(e)}", status=500)

async def trigger_other(request):
    """API endpoint to trigger other sources check."""
    global bot, logger
    
    if not bot:
        return web.Response(text="Bot not initialized", status=500)
    
    try:
        data = await request.json()
        category = data.get('category', None)
        
        # Validate category if provided
        if category and category not in ['ai_news', 'hackathon_news', 'tech_news', 'startup_news']:
            return web.Response(text=f"Invalid category: {category}", status=400)
        
        # Get the first text channel to use for context
        channel = None
        for guild in bot.guilds:
            for ch in guild.text_channels:
                channel = ch
                break
            if channel:
                break
                
        if not channel:
            return web.Response(text="No text channel available", status=500)
            
        # Create a mock context
        class MockContext:
            async def send(self, message):
                logger.info(f"API trigger message: {message}")
                
        ctx = MockContext()
        
        # Trigger the other sources check
        await bot.manual_other_sources_check(ctx, category)
        
        return web.Response(
            text=f"Other sources check triggered successfully{f' for category: {category}' if category else ''}",
            status=200
        )
    except Exception as e:
        logger.error(f"Error in trigger_other API: {str(e)}")
        return web.Response(text=f"Error: {str(e)}", status=500)

async def trigger_all(request):
    """API endpoint to trigger all news sources."""
    global bot, logger
    
    if not bot:
        return web.Response(text="Bot not initialized", status=500)
    
    try:
        data = await request.json()
        category = data.get('category', None)
        
        # Validate category if provided
        if category and category not in ['ai_news', 'hackathon_news', 'tech_news', 'startup_news']:
            return web.Response(text=f"Invalid category: {category}", status=400)
        
        # Get the first text channel to use for context
        channel = None
        for guild in bot.guilds:
            for ch in guild.text_channels:
                channel = ch
                break
            if channel:
                break
                
        if not channel:
            return web.Response(text="No text channel available", status=500)
            
        # Create a mock context
        class MockContext:
            async def send(self, message):
                logger.info(f"API trigger message: {message}")
                
        ctx = MockContext()
        
        # Trigger both checks
        await bot.manual_rss_check(ctx, category)
        await bot.manual_other_sources_check(ctx, category)
        
        return web.Response(
            text=f"All news sources triggered successfully{f' for category: {category}' if category else ''}",
            status=200
        )
    except Exception as e:
        logger.error(f"Error in trigger_all API: {str(e)}")
        return web.Response(text=f"Error: {str(e)}", status=500)

async def start_api_server():
    """Start the API server."""
    global logger
    
    app = web.Application()
    app.add_routes([
        web.get('/health', health_check),
        web.post('/api/trigger/rss', trigger_rss),
        web.post('/api/trigger/other', trigger_other),
        web.post('/api/trigger/all', trigger_all)
    ])
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    
    logger.info("API server started on http://0.0.0.0:8080")

def run_api_server():
    """Run the API server in a separate thread."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_api_server())
    loop.run_forever()

def main():
    # Initialize logger
    global logger, bot
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
        
        # Start API server in a separate thread
        api_thread = threading.Thread(target=run_api_server, daemon=True)
        api_thread.start()
        logger.info("API server thread started")
        
        # Run the bot
        bot.run(os.getenv('DISCORD_TOKEN'))
    except Exception as e:
        logger.error(f"Error running bot: {str(e)}")
        
if __name__ == "__main__":
    main() 