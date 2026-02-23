import json
import time
from twikit import Client
from datetime import datetime
import os
import asyncio
from pathlib import Path

# Configuration - Docker-friendly paths
# BASE_DIR = Path('/app/data')  # Use app data directory instead of home
# BASE_DIR.mkdir(exist_ok=True, parents=True)  # Create directory if it doesn't exist

BASE_DIR = Path.cwd()  # Use current working directory

COOKIES_FILE = BASE_DIR / 'twitter_cookies.json'
CREDENTIALS_FILE = BASE_DIR / 'twitter_credentials.json'
MIN_REQUEST_INTERVAL = 2.0
LAST_REQUEST_TIME = 0

def wait_for_rate_limit():
    """Ensure we don't exceed rate limits"""
    global LAST_REQUEST_TIME
    current_time = time.time()
    time_since_last = current_time - LAST_REQUEST_TIME
    
    if time_since_last < MIN_REQUEST_INTERVAL:
        sleep_time = MIN_REQUEST_INTERVAL - time_since_last
        time.sleep(sleep_time)
    
    LAST_REQUEST_TIME = time.time()

def load_credentials():
    """Load saved credentials"""
    try:
        with open(CREDENTIALS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"❌ Failed to load credentials: {e}")
        return None

def load_session(client):
    """Load saved session using twikit's built-in methods"""
    try:
        if not COOKIES_FILE.exists():
            print(f"ℹ️ No saved session found at {COOKIES_FILE}")
            return False
        
        client.load_cookies(str(COOKIES_FILE))
        print(f"✅ Session loaded from {COOKIES_FILE}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to load session: {e}")
        return False

def save_session(client):
    """Save session cookies"""
    try:
        # Ensure directory exists and is writable
        BASE_DIR.mkdir(exist_ok=True, parents=True)
        client.save_cookies(str(COOKIES_FILE))
        print(f"✅ Session saved to {COOKIES_FILE}")
        return True
    except PermissionError as e:
        print(f"❌ Permission denied saving session: {e}")
        print(f"💡 Make sure /app/data directory is writable")
        return False
    except Exception as e:
        print(f"❌ Failed to save session: {e}")
        return False

def login_sync(client):
    """Synchronous login function"""
    # Try to load saved credentials
    creds = load_credentials()
    
    if creds:
        print("📋 Found saved credentials")
        username = creds['username']
        email = creds['email']
        password = creds['password']
    else:
        # In Docker, we'll use environment variables instead of input
        username = os.getenv('TWITTER_USERNAME')
        email = os.getenv('TWITTER_EMAIL')
        password = os.getenv('TWITTER_PASSWORD')
        
        if not all([username, password]):
            print("❌ Twitter credentials not found in environment variables")
            print("💡 Set TWITTER_USERNAME, TWITTER_EMAIL, TWITTER_PASSWORD")
            return False
    
    try:
        # Run async login in sync context
        async def async_login():
            await client.login(
                auth_info_1=username,
                auth_info_2=email or username,
                password=password
            )
        
        asyncio.run(async_login())
        print("✅ Login successful!")
        
        # Save session
        save_session(client)
        return True
        
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return False

def search_tweets_sync(query, max_results=10):
    """
    Synchronous function to search tweets with authentication
    
    Args:
        query (str): Search query
        max_results (int): Maximum number of tweets to return (default: 10)
        
    Returns:
        dict: Contains either 'data' with tweet list or 'error' message
    """
    # Initialize client
    client = Client('en-US')
    
    print(f"🔍 Looking for session file at: {COOKIES_FILE}")
    
    # Try to load session or login
    if not load_session(client):
        if not login_sync(client):
            return {"error": "Authentication failed"}
    
    # Rate limiting
    wait_for_rate_limit()
    
    try:
        # Run async search in sync context
        async def async_search():
            return await client.search_tweet(
                query=f"{query} lang:id",
                product='Latest',
                count=max_results
            )
            
        # Execute the async search
        tweets = asyncio.run(async_search())
        
        if not tweets:
            return {"error": "No tweets found"}
            
        # Convert tweets to dict format
        tweet_data = []
        for tweet in tweets[:max_results]:
            tweet_info = {
                'id': tweet.id,
                'text': tweet.text,
                'created_at': tweet.created_at,
                'author': {
                    'name': tweet.user.name,
                    'screen_name': tweet.user.screen_name,
                    'followers_count': getattr(tweet.user, 'followers_count', 0)
                },
                'metrics': {
                    'likes': tweet.favorite_count or 0,
                    'retweets': tweet.retweet_count or 0,
                    'replies': getattr(tweet, 'reply_count', 0)
                },
                'url': f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"
            }
            tweet_data.append(tweet_info)
            
        return {"data": tweet_data}
        
    except Exception as e:
        return {"error": str(e)}

# Example usage
if __name__ == "__main__":
    # Example search
    query = "python programming"
    print(f"🔍 Searching for: {query}")
    
    results = search_tweets_sync(query, max_results=5)
    
    if "error" in results:
        print(f"Error: {results['error']}")
    else:
        for tweet in results["data"]:
            print(f"\\n{'='*50}")
            print(f"Author: @{tweet['author']['screen_name']}")
            print(f"Text: {tweet['text']}")
            print(f"Likes: {tweet['metrics']['likes']}")
            print(f"URL: {tweet['url']}")