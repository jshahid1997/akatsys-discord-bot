"""
Main Discord bot class for handling news distribution.
"""

import discord
from discord.ext import commands, tasks
from datetime import datetime, timezone
from src.services.news_service import NewsService
from src.services.summarizer import GeminiSummarizer
from src.utils.logger import Logger
from src.constants.app_constants import (
    CHANNEL_IDS,
    INTERVALS,
    EMBED_COLORS
)

class NewsBot(commands.Bot):
    def __init__(self):
        """Initialize the NewsBot with required services and configurations."""
        # Set up intents
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)
        
        # Initialize logger
        self.logger = Logger(__name__)
        
        # Initialize services
        self.news_service = NewsService()
        self.summarizer = GeminiSummarizer()
        
        # Start background tasks
        self.start_tasks()
        
    def start_tasks(self):
        """Initialize and start background tasks."""
        self.background_tasks = [
            self.check_rss_feeds,
            self.fetch_other_sources
        ]
        
    async def setup_hook(self):
        """Set up the bot and start background tasks."""
        self.logger.info("Starting bot setup...")
        for task in self.background_tasks:
            task.start()
        self.logger.info("Bot setup completed")
        
    @tasks.loop(seconds=INTERVALS['RSS_CHECK'])
    async def check_rss_feeds(self):
        """Check RSS feeds for new content."""
        self.logger.info("Starting RSS feed check")
        
        for category in ['ai_news', 'hackathon_news', 'tech_news', 'startup_news']:
            channel_id = CHANNEL_IDS.get(category.upper())
            if not channel_id:
                continue
                
            channel = self.get_channel(channel_id)
            if not channel:
                self.logger.warning(f"Channel not found for category: {category}")
                continue
                
            try:
                news_items = await self.news_service.fetch_rss_news(category)
                for item in news_items:
                    summary = await self.summarizer.summarize(item['title'], item['description'])
                    embed = self.create_news_embed(item, summary, category)
                    await channel.send(embed=embed)
                    self.news_service.mark_as_processed(item['id'])
                    
            except Exception as e:
                self.logger.error(f"Error processing RSS feeds for {category}: {str(e)}")
                
    @tasks.loop(seconds=INTERVALS['OTHER_SOURCES'])
    async def fetch_other_sources(self):
        """Fetch news from YouTube and Google News."""
        self.logger.info("Starting other sources check")
        
        for category in ['ai_news', 'hackathon_news', 'tech_news', 'startup_news']:
            channel_id = CHANNEL_IDS.get(category.upper())
            if not channel_id:
                continue
                
            channel = self.get_channel(channel_id)
            if not channel:
                self.logger.warning(f"Channel not found for category: {category}")
                continue
                
            try:
                # Fetch YouTube videos
                videos = await self.news_service.fetch_youtube_news(category)
                for video in videos:
                    summary = await self.summarizer.summarize(video['title'], video['description'])
                    embed = self.create_youtube_embed(video, summary, category)
                    await channel.send(embed=embed)
                    self.news_service.mark_as_processed(video['id'])
                    
                # Fetch Google News articles
                articles = await self.news_service.fetch_google_news(category)
                for article in articles:
                    summary = await self.summarizer.summarize(article['title'], article['description'])
                    embed = self.create_news_embed(article, summary, category)
                    await channel.send(embed=embed)
                    self.news_service.mark_as_processed(article['id'])
                    
            except Exception as e:
                self.logger.error(f"Error processing other sources for {category}: {str(e)}")
                
    def create_news_embed(self, item: dict, summary: str, category: str) -> discord.Embed:
        """Create a Discord embed for news items."""
        embed = discord.Embed(
            title=item['title'],
            url=item.get('url') or item.get('link'),
            description=summary,
            color=EMBED_COLORS[category.upper()],
            timestamp=datetime.now(timezone.utc)
        )
        embed.add_field(name="Source", value=item['source'], inline=False)
        embed.set_footer(text=f"News Bot - {category.replace('_', ' ').title()}")
        return embed
        
    def create_youtube_embed(self, video: dict, summary: str, category: str) -> discord.Embed:
        """Create a Discord embed for YouTube videos."""
        embed = discord.Embed(
            title=video['title'],
            url=video['url'],
            description=summary,
            color=EMBED_COLORS[category.upper()],
            timestamp=datetime.now(timezone.utc)
        )
        embed.set_thumbnail(url=video['thumbnail'])
        embed.set_footer(text=f"YouTube - {category.replace('_', ' ').title()}")
        return embed
        
    @check_rss_feeds.before_loop
    @fetch_other_sources.before_loop
    async def before_tasks(self):
        """Wait for the bot to be ready before starting tasks."""
        await self.wait_until_ready()
        self.logger.info("Bot is ready, starting background tasks") 