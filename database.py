from pymongo import MongoClient
from config import MONGO_DB_URI, MONGO_DB_NAME

# MongoDB setup
client = MongoClient(MONGO_DB_URI)
db = client[MONGO_DB_NAME]

def store_post_data(post_data, topic):
    """Store fetched post data in the MongoDB collection."""
    collection = db[topic]
    collection.insert_one(post_data)

def store_subreddit_stats(stats, subreddit_name):
    """Store subreddit statistics in a MongoDB collection."""
    collection = db['subreddit_stats']
    # Insert new document instead of updating
    collection.insert_one(stats)
