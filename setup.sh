#!/bin/bash

# Create logs directory if it doesn't exist
mkdir -p logs

# Set permissions for logs directory
chmod 777 logs

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cat > .env << EOL
DISCORD_TOKEN=your_discord_token
YOUTUBE_API_KEY=your_youtube_api_key
NEWS_API_KEY=your_google_api_key
GEMINI_API_KEY=your_gemini_api_key
EOL
    echo "Please update .env file with your API keys"
fi

# Make the script executable
chmod +x setup.sh 