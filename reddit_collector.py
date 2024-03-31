import praw
from datetime import datetime
from config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT
from database import store_post_data, store_subreddit_stats
from database import db

# Initialize Reddit API client
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

def fetch_subreddit_stats(subreddit_name):
    """Fetch and return general statistics for a subreddit."""
    subreddit = reddit.subreddit(subreddit_name)
    stats = {
        "name": subreddit.display_name,
        "title": subreddit.title,
        "subscribers": subreddit.subscribers,
        "active_users": subreddit.active_user_count,
        "description": subreddit.public_description,
        "created_utc": datetime.utcfromtimestamp(subreddit.created_utc)
    }
    store_subreddit_stats(stats, subreddit_name)

def fetch_and_store_posts(topic, subreddits, sort_orders=['new'], limit=10):
    """Fetch and store posts from multiple subreddits for a given topic in a topic-specific collection."""
    collection = db[topic]  # Create or select a collection based on the topic name
    for sort_order in sort_orders:
        for subreddit_name in subreddits:
            if sort_order == 'hot':
                posts = reddit.subreddit(subreddit_name).hot(limit=limit)
            elif sort_order == 'top':
                posts = reddit.subreddit(subreddit_name).top(time_filter='day', limit=limit)
            elif sort_order == 'rising':
                posts = reddit.subreddit(subreddit_name).rising(limit=limit)
            else:  # default to 'new'
                posts = reddit.subreddit(subreddit_name).new(limit=limit)

            for post in posts:
                # Ensure the author attribute is accessed safely
                author_flair_text = post.author_flair_text if post.author else "N/A"
                post_data = {
                    "subreddit": subreddit_name,
                    "sort_order": sort_order,
                    "title": post.title,
                    "score": post.score,
                    "id": post.id,
                    "url": post.url,
                    "created_utc": datetime.utcfromtimestamp(post.created_utc),
                    "num_comments": post.num_comments,
                    "body": post.selftext,
                    "upvote_ratio": post.upvote_ratio,
                    "awards": post.gildings,
                    "post_flair": post.link_flair_text,
                    "user_flair": author_flair_text,
                    "crossposts": post.num_crossposts,
                    "domain": post.domain,
                    "is_stickied": post.stickied
                }
                collection.insert_one(post_data)
            print(f"Finished fetching and storing {sort_order} posts from /r/{subreddit_name} for {topic}.")
