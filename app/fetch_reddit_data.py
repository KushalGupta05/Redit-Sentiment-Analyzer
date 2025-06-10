import os
import praw # Python Reddit API Wrapper
from dotenv import load_dotenv # For loading environment variables

# Load environment variables from .env file (if not already loaded by app.py)
load_dotenv()

def fetch_reddit_data(topic, limit=10):
    """
    Fetches Reddit posts based on a given topic.

    Args:
        topic (str): The search query for Reddit posts.
        limit (int): The maximum number of posts to fetch. Defaults to 10.

    Returns:
        list: A list of dictionaries, where each dictionary represents a post
              with 'title', 'content', and 'url' keys.
              Returns an empty list if an error occurs.
    """
    try:
        # Initialize PRAW Reddit instance with credentials from environment variables
        reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT')
        )
        # Set Reddit instance to read-only mode for safety and performance
        reddit.read_only = True

        posts = []
        # Access the 'all' subreddit (or a specific subreddit if needed)
        subreddit = reddit.subreddit('all')

        # Search for submissions within the subreddit
        # Using 'new' sort and 'all' time_filter to get recent relevant posts
        for submission in subreddit.search(topic, sort='new', time_filter='all', limit=limit):
            # Append post details to the list
            posts.append({
                'title': submission.title,
                
                'content': submission.selftext or 'No Content Available',
                'url': submission.url
            })
        return posts
    except Exception as e:
        
        print(f"Error fetching data from Reddit: {e}")
        return [] # Return empty list on error
