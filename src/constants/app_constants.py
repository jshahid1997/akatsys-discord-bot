"""
Constants for the Discord News Bot application.
"""

# Channel Configuration
CHANNEL_IDS = {
    'AI_NEWS': 1342736251022872636,
    'HACKATHON_NEWS': 1341818303630413895,
    'TECH_NEWS': 1342767292320186470,
    'STARTUP_NEWS': 1342767356224602202
}

# Time Intervals (in seconds)
INTERVALS = {
    'RSS_CHECK': 7200,  # 2 hours
    'OTHER_SOURCES': 21600  # 6 hours
}

# RSS Feed URLs
RSS_FEEDS = {
    'ai_news': [
        'https://arxiv.org/rss/cs.AI',
        'https://blogs.nvidia.com/feed/',
        'https://www.reddit.com/r/artificial/.rss',
        'https://www.reddit.com/r/ArtificialInteligence/.rss',
        'https://www.wired.com/feed/tag/ai/latest/rss'
    ],
    'hackathon_news': [
        'https://devpost.com/feed'
    ],
    'tech_news': [
        'https://techcrunch.com/feed/',
        'https://www.theverge.com/rss/index.xml',
        'https://www.pcmag.com/feeds/rss/latest',
        'https://www.reddit.com/r/technology/.rss',
        'https://www.reddit.com/r/TechNews/.rss'
    ],
    'startup_news': [
        'https://news.crunchbase.com/feed/'
    ]
}

# Search Queries
SEARCH_QUERIES = {
    'ai_news': 'artificial intelligence news',
    'hackathon_news': 'AI hackathon news',
    'tech_news': 'latest technology news',
    'startup_news': 'startup news'
}

# Embed Colors
EMBED_COLORS = {
    'AI_NEWS': 0x3498db,  # Blue
    'HACKATHON_NEWS': 0x2ecc71,  # Green
    'TECH_NEWS': 0xe74c3c,  # Red
    'STARTUP_NEWS': 0xf1c40f  # Yellow
}

# Maximum Results
MAX_RESULTS = {
    'RSS_FEED': 10,
    'YOUTUBE': 1,
    'GOOGLE_NEWS': 5
}

# Gemini Configuration
GEMINI_PROMPT = """
Summarize the following news article in 2-3 sentences. Focus on the key points and maintain a neutral tone.
Keep the summary concise and informative.

Title: {title}
Content: {content}
Sources: {sources}
""" 