from reddit_collector import fetch_and_store_posts, fetch_subreddit_stats
from config import TOPICS, SORT_ORDERS
from email_notifications import send_email_notification

def main():
    try:
        for topic, subreddits in TOPICS.items():
            for subreddit_name in subreddits:
                # Fetch and store stats for each subreddit
                fetch_subreddit_stats(subreddit_name)
            
            # Fetch and store posts for each topic and its subreddits
            fetch_and_store_posts(topic, subreddits, SORT_ORDERS)
        
        send_email_notification("Reddit Scraper - Success", "Data collection complete for all topics.")
    except Exception as e:
        send_email_notification("Reddit Scraper - Error", f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    main()