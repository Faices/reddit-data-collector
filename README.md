# Reddit Data Collector

The Reddit Data Collector is a Python application designed to scrape and store data from specified subreddits. It focuses on collecting posts and their statistics to analyze trends, particularly in topics like Bitcoin, Stocks, CryptoCurrency, Data Science, and News. The application also features email notifications for successful executions or failures, enhancing monitoring and maintenance capabilities.

## Features

- Data scraping from multiple subreddits
- Collection of subreddit statistics (e.g., subscribers, active users)
- Storing data in MongoDB for analysis
- Email notifications on script completion and errors

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.9+
- MongoDB
- A Reddit API key
- SMTP server access for email notifications (Gmail used in examples)

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://your-repository-url.git

2. **Navigate to the project directory:**
    ```bash
    cd RedditDataCollector

3. **Create a virtual environment and activate it:**
macOS/Linux:
    ```bash
    python3 -m venv venv
    source venv/bin/activate

4. **Install the required packages:**
    ```bash
    pip install -r requirements.txt

5. **Set up your .env file with the necessary environment variables:**
    ```plaintext
    REDDIT_CLIENT_ID=your_client_id
    REDDIT_CLIENT_SECRET=your_client_secret
    REDDIT_USER_AGENT='your_user_agent'
    MONGO_DB_URI='your_mongo_db_uri'
    MONGO_DB_NAME='your_mongo_db_name'
    SENDER_EMAIL='your_sender_email'
    RECEIVER_EMAIL='your_receiver_email'
    EMAIL_APP_PASSWORD='your_email_app_password'

### Modular Structure
The application is structured into several modules for better maintainability and separation of concerns:

- config.py: Contains configuration variables and settings.
- email_notifications.py: Handles sending email notifications.
- reddit_collector.py: Core functionality for collecting data from Reddit.
- database.py: Manages database interactions.
- main.py: Orchestrates the data collection process.

### Usage
Run the script:
    ```bash
    python main.py

### Docker Support
To build and run the application using Docker, follow these steps:

1. Build the Docker image:
    ```bash
    docker build -t reddit-data-collector .

2. Run the container:
    ```bash
    docker run --name reddit-data-collector --env-file .env reddit-data-collector


### Acknowledgments
- Thanks to the Reddit API for providing access to subreddit data.
- Appreciation for MongoDB, which makes data storage and retrieval efficient.
- Gratitude towards the Python community for the excellent libraries and tools.