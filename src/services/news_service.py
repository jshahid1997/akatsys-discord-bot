"""
Service for handling different news sources (RSS, YouTube, Google News).
"""

import feedparser
from googleapiclient.discovery import build
import aiohttp
from src.utils.logger import Logger
from src.constants.app_constants import RSS_FEEDS, SEARCH_QUERIES, MAX_RESULTS
import os

class NewsService:
    def __init__(self):
        self.logger = Logger(__name__)
        self.youtube_api_key = os.getenv('YOUTUBE_API_KEY')
        self.news_api_key = os.getenv('NEWS_API_KEY')
        self.processed_items = set()
        
    async def fetch_rss_news(self, category: str) -> list:
        """
        Fetch news from RSS feeds for a specific category.
        
        Args:
            category (str): News category
            
        Returns:
            list: List of news items
        """
        news_items = []
        feeds = RSS_FEEDS.get(category, [])
        
        for feed_url in feeds:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries[:MAX_RESULTS['RSS_FEED']]:
                    item_id = f"{feed_url}_{entry.id}"
                    
                    if item_id not in self.processed_items:
                        news_items.append({
                            'id': item_id,
                            'title': entry.title,
                            'link': entry.link,
                            'description': entry.description,
                            'source': feed_url
                        })
                        
                self.logger.info(f"Successfully fetched RSS feed: {feed_url}")
                        
            except Exception as e:
                self.logger.error(f"Error fetching RSS feed {feed_url}: {str(e)}")
                continue
                
        return news_items
        
    async def fetch_youtube_news(self, category: str) -> list:
        """
        Fetch news from YouTube for a specific category.
        
        Args:
            category (str): News category
            
        Returns:
            list: List of YouTube videos
        """
        if not self.youtube_api_key:
            self.logger.error("YouTube API key not found")
            return []
            
        try:
            youtube = build('youtube', 'v3', developerKey=self.youtube_api_key)
            query = SEARCH_QUERIES.get(category, '')
            
            search_response = youtube.search().list(
                q=query,
                part='snippet',
                type='video',
                order='date',
                maxResults=MAX_RESULTS['YOUTUBE']
            ).execute()
            
            videos = []
            for item in search_response['items']:
                video_id = item['id']['videoId']
                if video_id not in self.processed_items:
                    videos.append({
                        'id': video_id,
                        'title': item['snippet']['title'],
                        'description': item['snippet']['description'],
                        'thumbnail': item['snippet']['thumbnails']['default']['url'],
                        'url': f"https://www.youtube.com/watch?v={video_id}"
                    })
                    
            self.logger.info(f"Successfully fetched YouTube videos for category: {category}")
            return videos
            
        except Exception as e:
            self.logger.error(f"Error fetching YouTube content for {category}: {str(e)}")
            return []
            
    async def fetch_google_news(self, category: str) -> list:
        """
        Fetch news from Google News API for a specific category.
        
        Args:
            category (str): News category
            
        Returns:
            list: List of news articles
        """
        if not self.news_api_key:
            self.logger.error("Google API key not found")
            return []
            
        try:
            async with aiohttp.ClientSession() as session:
                query = SEARCH_QUERIES.get(category, '')
                url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&apiKey={self.news_api_key}"
                
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        articles = []
                        
                        for article in data['articles'][:MAX_RESULTS['GOOGLE_NEWS']]:
                            article_id = f"google_{article['url']}"
                            if article_id not in self.processed_items:
                                articles.append({
                                    'id': article_id,
                                    'title': article['title'],
                                    'description': article['description'],
                                    'url': article['url'],
                                    'source': article['source']['name']
                                })
                                
                        self.logger.info(f"Successfully fetched Google News for category: {category}")
                        return articles
                    else:
                        self.logger.error(f"Error fetching Google News: {response.status}")
                        return []
                        
        except Exception as e:
            self.logger.error(f"Error fetching Google News for {category}: {str(e)}")
            return []
            
    def mark_as_processed(self, item_id: str):
        """Mark an item as processed."""
        self.processed_items.add(item_id) 