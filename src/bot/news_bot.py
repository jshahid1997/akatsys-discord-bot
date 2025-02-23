"""
Main Discord bot class for handling news distribution.
"""

import discord
from discord.ext import commands, tasks
from datetime import datetime, timezone
import asyncio
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
        # Set up intents with all required permissions
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.guild_messages = True
        intents.guild_reactions = True
        
        # Initialize the bot with required permissions
        super().__init__(
            command_prefix='!',
            intents=intents,
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="news feeds"
            )
        )
        
        # Initialize logger
        self.logger = Logger(__name__)
        
        # Initialize services
        self.news_service = NewsService()
        self.summarizer = GeminiSummarizer()
        
        # Start background tasks
        self.start_tasks()

    async def on_ready(self):
        """Called when the bot is ready and connected to Discord."""
        self.logger.info(f"Logged in as {self.user.name} ({self.user.id})")
        self.logger.info(f"Connected to {len(self.guilds)} guilds:")
        for guild in self.guilds:
            self.logger.info(f"- {guild.name} (ID: {guild.id})")
            # Log available channels
            self.logger.info(f"Available channels in {guild.name}:")
            for channel in guild.text_channels:
                self.logger.info(f"- {channel.name} (ID: {channel.id})")
        
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
            self.logger.info(f"Processing RSS feeds for category: {category}")
            channel_id = CHANNEL_IDS.get(category.upper())
            if not channel_id:
                self.logger.warning(f"No channel ID configured for category: {category}")
                continue
                
            channel = self.get_channel(channel_id)
            if not channel:
                # Try to find channel by name if ID doesn't work
                category_name = category.replace('_', '-')
                for guild in self.guilds:
                    channel = discord.utils.get(guild.text_channels, name=category_name)
                    if channel:
                        break
                
                if not channel:
                    self.logger.warning(f"Channel not found for category: {category}")
                    continue
                
            try:
                # Fetch all news items
                news_items = await self.news_service.fetch_rss_news(category)
                if not news_items:
                    continue
                    
                # Get a batch summary
                summary = await self.summarizer.summarize_batch(category, news_items)
                
                # Create and send the embed
                embed = discord.Embed(
                    description=summary,
                    color=EMBED_COLORS[category.upper()],
                    timestamp=datetime.now(timezone.utc)
                )
                embed.set_footer(text=f"News Bot - {category.replace('_', ' ').title()}")
                
                await channel.send(embed=embed)
                
                # Mark all items as processed
                for item in news_items:
                    self.news_service.mark_as_processed(item['id'])
                    
            except discord.Forbidden:
                self.logger.error(f"Bot doesn't have permission to send messages in channel: {channel.name}")
            except Exception as e:
                self.logger.error(f"Error processing RSS feeds for {category}: {str(e)}")
            
            # Add timeout between categories
            if category != 'startup_news':  # Don't wait after the last category
                self.logger.info(f"Waiting 300 seconds before processing next category...")
                await asyncio.sleep(300)
                
    @tasks.loop(seconds=INTERVALS['OTHER_SOURCES'])
    async def fetch_other_sources(self):
        """Fetch news from YouTube and Google News."""
        self.logger.info("Starting other sources check")
        
        for category in ['ai_news', 'hackathon_news', 'tech_news', 'startup_news']:
            self.logger.info(f"Processing other sources for category: {category}")
            channel_id = CHANNEL_IDS.get(category.upper())
            if not channel_id:
                self.logger.warning(f"No channel ID configured for category: {category}")
                continue
                
            channel = self.get_channel(channel_id)
            if not channel:
                # Try to find channel by name if ID doesn't work
                category_name = category.replace('_', '-')
                for guild in self.guilds:
                    channel = discord.utils.get(guild.text_channels, name=category_name)
                    if channel:
                        break
                
                if not channel:
                    self.logger.warning(f"Channel not found for category: {category}")
                    continue
                
            try:
                # Fetch all news items
                all_items = []
                
                # Fetch YouTube videos
                videos = await self.news_service.fetch_youtube_news(category)
                all_items.extend(videos)
                
                # Fetch Google News articles
                articles = await self.news_service.fetch_google_news(category)
                all_items.extend(articles)
                
                if not all_items:
                    continue
                    
                # Get a batch summary
                summary = await self.summarizer.summarize_batch(category, all_items)
                
                # Create and send the embed
                embed = discord.Embed(
                    description=summary,
                    color=EMBED_COLORS[category.upper()],
                    timestamp=datetime.now(timezone.utc)
                )
                embed.set_footer(text=f"News Bot - {category.replace('_', ' ').title()}")
                
                await channel.send(embed=embed)
                
                # Mark all items as processed
                for item in all_items:
                    self.news_service.mark_as_processed(item['id'])
                    
            except discord.Forbidden:
                self.logger.error(f"Bot doesn't have permission to send messages in channel: {channel.name}")
            except Exception as e:
                self.logger.error(f"Error processing other sources for {category}: {str(e)}")
            
            # Add timeout between categories
            if category != 'startup_news':  # Don't wait after the last category
                self.logger.info(f"Waiting 300 seconds before processing next category...")
                await asyncio.sleep(300)
                
    @check_rss_feeds.before_loop
    @fetch_other_sources.before_loop
    async def before_tasks(self):
        """Wait for the bot to be ready before starting tasks."""
        await self.wait_until_ready()
        self.logger.info("Bot is ready, starting background tasks") 