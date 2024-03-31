from reddit_collector import fetch_and_store_posts
from config import TOPICS, SORT_ORDERS
from email_notifications import send_email_notification

def main():
    try:
        for topic, subreddits in TOPICS.items():
            fetch_and_store_posts(topic, subreddits, SORT_ORDERS)
        send_email_notification("Reddit Scraper - Success", "Data collection complete for all topics.")
    except Exception as e:
        send_email_notification("Reddit Scraper - Error", f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    main()