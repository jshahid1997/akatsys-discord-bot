# Discord News Bot

A Discord bot that automatically fetches and posts news from various sources to specific channels. The bot supports multiple news categories and sources, with AI-powered summarization using Google's Gemini.

## Features

- **Multiple News Categories**:
  - AI News
  - Hackathon News
  - Tech News
  - Startup News

- **Multiple Sources**:
  - RSS Feeds
  - YouTube Videos
  - Google News Articles

- **Smart Summarization**:
  - AI-powered content summarization using Google Gemini
  - Concise and relevant summaries

- **Real-time Updates**:
  - Automatic RSS feed checking every 30 minutes
  - Other sources checked every 6 hours
  - Immediate posting of new content

## Prerequisites

- Python 3.8 or higher (for local installation)
- Docker and Docker Compose (for Docker installation)
- Discord Bot Token
- Google API Key
- YouTube API Key
- Gemini API Key

## Installation

### Using Docker (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/discord-news-bot.git
   cd discord-news-bot
   ```

2. Create a `.env` file in the root directory with your API keys:
   ```env
   DISCORD_TOKEN=your_discord_token
   YOUTUBE_API_KEY=your_youtube_api_key
   NEWS_API_KEY=your_google_api_key
   GEMINI_API_KEY=your_gemini_api_key
   ```

3. Build and start the container:
   ```bash
   docker-compose up -d
   ```

4. View logs:
   ```bash
   docker-compose logs -f
   ```

### Local Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/discord-news-bot.git
   cd discord-news-bot
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with your API keys:
   ```env
   DISCORD_TOKEN=your_discord_token
   YOUTUBE_API_KEY=your_youtube_api_key
   NEWS_API_KEY=your_google_api_key
   GEMINI_API_KEY=your_gemini_api_key
   ```

## Configuration

The bot's configuration is stored in `src/constants/app_constants.py`. You can modify:

- Channel IDs
- Time intervals
- RSS feed sources
- Search queries
- Maximum results per source
- Embed colors

## Usage

### Docker Usage

1. Start the bot:
   ```bash
   docker-compose up -d
   ```

2. Stop the bot:
   ```bash
   docker-compose down
   ```

3. View logs:
   ```bash
   docker-compose logs -f
   ```

4. Restart the bot:
   ```bash
   docker-compose restart
   ```

### Local Usage

1. Start the bot:
   ```bash
   python main.py
   ```

The bot will automatically:
- Check RSS feeds every 30 minutes
- Check YouTube and Google News every 6 hours
- Post new content to the appropriate channels
- Summarize content using Gemini AI

## Project Structure

```
discord-news-bot/
├── main.py
├── Dockerfile
├── docker-compose.yml
├── src/
│   ├── __init__.py
│   ├── bot/
│   │   ├── __init__.py
│   │   └── news_bot.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── news_service.py
│   │   └── summarizer.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── logger.py
│   └── constants/
│       ├── __init__.py
│       └── app_constants.py
├── logs/
├── requirements.txt
├── .env
└── README.md
```

## Logging

The bot uses a comprehensive logging system that:
- Logs to both console and file
- Rotates log files daily
- Maintains the last 5 log files
- Logs all important events and errors

## Error Handling

The bot includes robust error handling:
- Graceful handling of API failures
- Automatic retries for transient errors
- Detailed error logging
- Fallback mechanisms for summarization

## Docker Health Checks

The Docker container includes health checks that:
- Monitor the existence of log files
- Check every 30 seconds
- Mark container as unhealthy if checks fail
- Automatically restart if needed

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 