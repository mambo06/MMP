#!/usr/bin/env python3
"""
Twitter API v2 Search Script with Rate Limiting
===============================================

This script searches for recent tweets using Twitter API v2 with proper
rate limiting, error handling, and a strict limit of 10 tweets per request.

Features:
- Rate limiting with automatic delays
- Retry mechanism with progressive backoff
- Comprehensive error handling
- Formatted output with tweet metrics
- Bearer token validation

Usage:
    python twitter_search.py

Author: Assistant
Date: June 2025
"""

import requests
import json
import time
from datetime import datetime
import urllib.parse


# Configuration
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAIlK2wEAAAAAk73SVLGvM6H6droHfpb5ryGCTa4%3DZsOYOwUf6zJVGb0ftHbGpQF401ms177dkIf3H3xICUwDUJCc7s'
MIN_REQUEST_INTERVAL = 1.0  # Minimum seconds between requests
MAX_TWEETS_PER_REQUEST = 10  # Strict limit

# Global variables for rate limiting
LAST_REQUEST_TIME = 0

def wait_for_rate_limit():
    """
    Ensure we don't exceed rate limits by waiting between requests.
    Twitter API v2 allows 300 requests per 15-minute window for search.
    """
    global LAST_REQUEST_TIME
    current_time = time.time()
    time_since_last = current_time - LAST_REQUEST_TIME
    
    if time_since_last < MIN_REQUEST_INTERVAL:
        sleep_time = MIN_REQUEST_INTERVAL - time_since_last
        print(f"⏳ Rate limiting: waiting {sleep_time:.1f} seconds...")
        time.sleep(sleep_time)
    
    LAST_REQUEST_TIME = time.time()

def search_tweets(query, max_results=10):
    """
    Search for recent tweets using X (Twitter) API v2.
    
    Args:
        query (str): Search query string
        max_results (int): Number of tweets to return (max 10)
    
    Returns:
        dict: API response or error information
    """
    # Enforce strict limit
    max_results = min(max_results, MAX_TWEETS_PER_REQUEST)
    encoded_query = urllib.parse.quote(query)
    
    # Construct the complete URL with query parameters
    url = f"https://api.x.com/2/tweets/search/recent?query={encoded_query} lang:id&max_results={10}&tweet.fields=created_at,public_metrics,author_id,context_annotations&expansions=author_id"


    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }
    
    # Respect rate limits
    wait_for_rate_limit()
    
    try:
        print(f"🔍 Searching: '{query}' (requesting {max_results} tweets)")
        response = requests.get(url, headers=headers, timeout=30)
        
        # Log response details
        print(f"📊 Status: {response.status_code}")
        rate_limit_remaining = response.headers.get('x-rate-limit-remaining', 'Unknown')
        rate_limit_reset = response.headers.get('x-rate-limit-reset', 'Unknown')
        print(f"📈 Rate limit remaining: {rate_limit_remaining}")
        
        if response.status_code == 200:
            data = response.json()
            tweet_count = len(data.get('data', []))
            print(f"✅ Successfully retrieved {tweet_count} tweets")
            return format_tweet_results(data)
            
        elif response.status_code == 429:
            # Rate limit exceeded
            reset_time = response.headers.get('x-rate-limit-reset')
            error_data = {"error": "Rate limit exceeded"}
            
            if reset_time:
                try:
                    reset_datetime = datetime.fromtimestamp(int(reset_time))
                    error_data.update({
                        "reset_time": reset_time,
                        "reset_datetime": reset_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                        "wait_seconds": int(reset_time) - int(time.time())
                    })
                except ValueError:
                    pass
            
            return error_data
            
        elif response.status_code == 401:
            return {"error": "Unauthorized - Invalid Bearer Token"}
        elif response.status_code == 403:
            return {"error": "Forbidden - Check API permissions"}
        elif response.status_code == 400:
            return {"error": f"Bad Request - {response.text}"}
        else:
            return {"error": f"HTTP {response.status_code}: {response.text}"}
            
    except requests.exceptions.Timeout:
        return {"error": "Request timeout - API took too long to respond"}
    except requests.exceptions.ConnectionError:
        return {"error": "Connection error - Check internet connection"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

def format_tweet_results(data):
    """
    Format tweet data for human-readable display.
    
    Args:
        data (dict): API response data
        
    Returns:
        str: Formatted output string
    """
    if "error" in data:
        error_msg = f"❌ Error: {data['error']}"
        
        if "reset_datetime" in data:
            error_msg += f"\n   ⏰ Rate limit resets at: {data['reset_datetime']}"
        if "wait_seconds" in data and data["wait_seconds"] > 0:
            error_msg += f"\n   ⏳ Wait {data['wait_seconds']} seconds before retry"
            
        return error_msg
    
    if "data" not in data or not data["data"]:
        return "❌ No tweets found for this query"
    
    tweets = data["data"]
    result = f"✅ Found {len(tweets)} tweets:\n\n"
    
    for i, tweet in enumerate(tweets, 1):
        result += f"{'='*50}\n"
        result += f"📱 Tweet {i}/{len(tweets)}\n"
        result += f"{'='*50}\n"
        result += f"🆔 ID: {tweet['id']}\n"
        result += f"📝 Text: {tweet['text']}\n"
        
        if 'created_at' in tweet:
            # Format the timestamp nicely
            try:
                created = datetime.fromisoformat(tweet['created_at'].replace('Z', '+00:00'))
                result += f"🕒 Created: {created.strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
            except:
                result += f"🕒 Created: {tweet['created_at']}\n"
        
        if 'public_metrics' in tweet:
            metrics = tweet['public_metrics']
            result += f"📊 Engagement: "
            result += f"👍 {metrics.get('like_count', 0)} likes | "
            result += f"🔄 {metrics.get('retweet_count', 0)} retweets | "
            result += f"💬 {metrics.get('reply_count', 0)} replies\n"
        
        result += "\n"
    
    return result

def safe_search_with_retry(query, max_results=10, max_retries=3):
    """
    Search tweets with automatic retry on rate limit errors.
    
    Args:
        query (str): Search query
        max_results (int): Number of tweets to return
        max_retries (int): Maximum retry attempts
        
    Returns:
        dict: Search results or error information
    """
    for attempt in range(max_retries):
        print(f"🚀 Attempt {attempt + 1}/{max_retries}")
        result = search_tweets(query, max_results)
        
        # Success case
        if "error" not in result:
            return result
        
        # Handle rate limit errors with progressive backoff
        if "Rate limit exceeded" in result.get("error", ""):
            if attempt < max_retries - 1:  # Don't wait on the last attempt
                wait_time = result.get("wait_seconds", 60 * (attempt + 1))
                wait_time = max(wait_time, 60)  # Minimum 1 minute wait
                
                print(f"⏰ Rate limit hit. Waiting {wait_time} seconds...")
                print(f"🔄 Will retry in {wait_time//60} minutes and {wait_time%60} seconds")
                
                # Show countdown for long waits
                if wait_time > 60:
                    for remaining in range(wait_time, 0, -30):
                        if remaining > 30:
                            print(f"⏳ {remaining//60}m {remaining%60}s remaining...")
                            time.sleep(30)
                        else:
                            time.sleep(remaining)
                            break
                else:
                    time.sleep(wait_time)
            else:
                print("❌ Max retries reached. Rate limit still active.")
                return result
        else:
            # Non-rate-limit error, don't retry
            print(f"❌ Non-recoverable error: {result.get('error')}")
            return result
    
    return {"error": "Max retries exceeded"}

def main():
    """Main function to demonstrate the Twitter search functionality."""
    print("🐦 Twitter API v2 Search Tool")
    print("=" * 50)
    
    # Default search query
    default_query = "mutasi kementerian keuangan"
    
    # You can modify this query or make it interactive
    search_query = default_query
    tweet_count = 10
    
    print(f"🎯 Query: '{search_query}'")
    print(f"📊 Requesting: {tweet_count} tweets")
    print("-" * 50)
    
    # Perform the search with retry capability
    results = safe_search_with_retry(search_query, max_results=tweet_count)
    
    # Display results
    print("\n" + "=" * 60)
    print("📋 SEARCH RESULTS")
    print("=" * 60)
    formatted_output = format_tweet_results(results)
    print(formatted_output)
    
    # Additional info
    if "error" not in results and "data" in results:
        print("\n" + "=" * 60)
        print("ℹ️  ADDITIONAL INFO")
        print("=" * 60)
        print(f"🔍 Query used: '{search_query}'")
        print(f"📊 Tweets returned: {len(results['data'])}")
        print(f"⏰ Search completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()