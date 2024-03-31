import os
from dotenv import load_dotenv

load_dotenv()

# Reddit API
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')

# MongoDB
MONGO_DB_URI = os.getenv('MONGO_DB_URI')
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME')

# Email
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')
EMAIL_APP_PASSWORD = os.getenv('EMAIL_APP_PASSWORD')

# Topics and sort orders
TOPICS = {
    "Bitcoin": ['Bitcoin', 'btc'],
    "Stocks": ['stocks', 'investing', 'wallstreetbets'],
    "CryptoCurrency": ['cryptocurrency', 'crypto', 'CryptoMoonShots', 'CryptoMarkets'],
    "DataScience": ['datascience', 'MachineLearning', 'learnmachinelearning'],
    "News": ['news', 'worldnews'],
}
SORT_ORDERS = ['hot', 'new', 'top', 'rising']
