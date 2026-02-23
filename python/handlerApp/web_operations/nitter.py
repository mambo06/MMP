import snscrape.modules.twitter as sntwitter
from datetime import datetime, timedelta
import pandas as pd
import time
import json

def format_date(date_str):
    """Convert date string to a more readable format"""
    try:
        if isinstance(date_str, str):
            date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S%z')
        else:
            date_obj = date_str
        return date_obj.strftime('%Y-%m-%d %H:%M:%S')
    except Exception:
        return str(date_str)

def search_tweets(query, max_results=10, since=None, until=None, lang=None):
    """
    Search for tweets with advanced filters
    
    Args:
        query (str): Search query
        max_results (int): Maximum number of tweets to return
        since (str): Start date in YYYY-MM-DD format
        until (str): End date in YYYY-MM-DD format
        lang (str): Language filter (e.g., 'en' for English)
    
    Returns:
        list: List of tweet dictionaries
    """
    search_query = query

    # Add language filter if specified
    if lang:
        search_query += f" lang:{lang}"

    # Add date filters if specified
    if since:
        search_query += f" since:{since}"
    if until:
        search_query += f" until:{until}"

    print(f"🔍 Searching with query: {search_query}")
    tweets = []
    
    try:
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(search_query).get_items()):
            if i >= max_results:
                break
                
            tweet_data = {
                'username': tweet.user.username,
                'user_displayname': tweet.user.displayname,
                'text': tweet.rawContent,
                'date': format_date(tweet.date),
                'likes': tweet.likeCount,
                'retweets': tweet.retweetCount,
                'replies': tweet.replyCount,
                'quote_count': tweet.quoteCount,
                'language': tweet.lang,
                'tweet_url': tweet.url,
                'hashtags': tweet.hashtags if tweet.hashtags else [],
                'mentions': [mention.username for mention in tweet.mentionedUsers] if tweet.mentionedUsers else [],
                'source': tweet.source if hasattr(tweet, 'source') else None,
            }
            
            # Add media information if available
            if hasattr(tweet, 'media'):
                media_urls = []
                for media in tweet.media:
                    if hasattr(media, 'fullUrl'):
                        media_urls.append(media.fullUrl)
                tweet_data['media_urls'] = media_urls

            tweets.append(tweet_data)
            
            # Progress indicator
            if (i + 1) % 5 == 0:
                print(f"📥 Retrieved {i + 1} tweets...")
                
        return tweets
                
    except Exception as e:
        print(f"❌ Error during scraping: {str(e)}")
        return []

def format_tweet_results(tweets):
    """
    Format tweet data for human-readable display
    
    Args:
        tweets (list): List of tweet dictionaries
    
    Returns:
        str: Formatted string of tweet information
    """
    if not tweets:
        return "❌ No tweets found for this query"
    
    result = f"✅ Found {len(tweets)} tweets:\n\n"
    
    for i, tweet in enumerate(tweets, 1):
        result += f"{'='*50}\n"
        result += f"📱 Tweet {i}/{len(tweets)}\n"
        result += f"{'='*50}\n"
        
        result += f"👤 User: @{tweet['username']} ({tweet['user_displayname']})\n"
        result += f"📝 Text: {tweet['text']}\n"
        result += f"🕒 Created: {tweet['date']}\n"
        result += f"💬 Replies: {tweet['replies']}\n"
        result += f"🔁 Retweets: {tweet['retweets']}\n"
        result += f"❤️ Likes: {tweet['likes']}\n"
        result += f"🔄 Quotes: {tweet['quote_count']}\n"
        result += f"🌐 Language: {tweet['language']}\n"
        result += f"🔗 URL: {tweet['tweet_url']}\n"
        
        if tweet['hashtags']:
            result += f"#️⃣ Hashtags: {', '.join(tweet['hashtags'])}\n"
            
        if tweet['mentions']:
            result += f"@ Mentions: {', '.join(tweet['mentions'])}\n"
            
        if tweet.get('media_urls'):
            result += f"📷 Media URLs: {', '.join(tweet['media_urls'])}\n"
            
        result += "\n"
    
    return result

def save_tweets_csv(tweets, filename="tweets.csv"):
    """
    Save tweets to a CSV file
    
    Args:
        tweets (list): List of tweet dictionaries
        filename (str): Output filename
    """
    if not tweets:
        print("❌ No tweets to save")
        return
        
    df = pd.DataFrame(tweets)
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"✅ Saved {len(tweets)} tweets to {filename}")

def save_tweets_json(tweets, filename="tweets.json"):
    """
    Save tweets to a JSON file
    
    Args:
        tweets (list): List of tweet dictionaries
        filename (str): Output filename
    """
    if not tweets:
        print("❌ No tweets to save")
        return
        
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(tweets, f, ensure_ascii=False, indent=2)
    print(f"✅ Saved {len(tweets)} tweets to {filename}")

def main():
    """Main function to demonstrate usage"""
    # Example search parameters
    query = "kementerian keuangan"
    max_results = 10
    lang = "en"
    since = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    print("🔍 Twitter Search Tool")
    print("=" * 50)
    print(f"Query: {query}")
    print(f"Language: {lang}")
    print(f"Since: {since}")
    print(f"Max results: {max_results}")
    print("=" * 50)
    
    # Search for tweets
    tweets = search_tweets(
        query=query,
        max_results=max_results,
        since=since,
        lang=lang
    )
    
    # Display results
    print("\n" + format_tweet_results(tweets))
    
    # Save results
    if tweets:
        save_tweets_csv(tweets)
        save_tweets_json(tweets)

if __name__ == "__main__":
    main()
