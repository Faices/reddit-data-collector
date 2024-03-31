import os
import praw
import logging
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

# Configuration
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')
MONGO_DB_URI = os.getenv('MONGO_DB_URI')
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME')

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Reddit API Setup
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

# MongoDB Setup
client = MongoClient(MONGO_DB_URI)
db = client[MONGO_DB_NAME]

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
    return stats

def store_subreddit_stats(stats):
    """Store subreddit stats with a timestamp, without overwriting."""
    collection = db.subreddit_stats_history  # Using a new collection for historical data
    # Add a timestamp for when the data is being stored
    stats['timestamp'] = datetime.utcnow()
    collection.insert_one(stats)


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
                post_data = {
                    "subreddit": subreddit_name,
                    "sort_order": sort_order,
                    "title": post.title,
                    "score": post.score,
                    "id": post.id,
                    "url": post.url,
                    "created_utc": datetime.utcfromtimestamp(post.created_utc),
                    "num_comments": post.num_comments,
                    "body": post.selftext
                }
                collection.insert_one(post_data)
            print(f"Finished fetching and storing {sort_order} posts from /r/{subreddit_name} for {topic}.")

def send_email_notification(subject, body):
    sender_email = os.getenv('SENDER_EMAIL')
    receiver_email = os.getenv('RECEIVER_EMAIL')
    password = os.getenv('EMAIL_APP_PASSWORD')

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print("Email notification sent successfully.")
    except Exception as e:
        print(f"Failed to send email notification: {e}")



if __name__ == "__main__":
    try:
        topics = {
            "Bitcoin": ['Bitcoin', 'btc'],
            "Stocks": ['stocks', 'investing', 'wallstreetbets'],
            "CryptoCurrency": ['cryptocurrency', 'crypto', 'CryptoMoonShots','CryptoMarkets'],
            "DataScience": ['datascience', 'MachineLearning', 'learnmachinelearning'],
            "News": ['news', 'worldnews'],
        }
        sort_orders = ['hot', 'new', 'top', 'rising']
        
        for topic, subreddits in topics.items():
            for subreddit_name in subreddits:
                stats = fetch_subreddit_stats(subreddit_name)
                store_subreddit_stats(stats)
                print(f"Stored historical stats for /r/{subreddit_name}.")
        
        for topic, subreddits in topics.items():
            fetch_and_store_posts(topic, subreddits, sort_orders)
        
        send_email_notification("Reddit Scraper - Success", "Data collection complete for all topics.")
    except Exception as e:
        send_email_notification("Reddit Scraper - Error", f"An error occurred: {e}")
        raise