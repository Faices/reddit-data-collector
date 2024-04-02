import streamlit as st
from pymongo import MongoClient
from config import MONGO_DB_URI, MONGO_DB_NAME

# MongoDB connection
client = MongoClient(MONGO_DB_URI )
db = client[MONGO_DB_NAME] # Change this to your database name

# Streamlit app
st.title('MongoDB Streamlit App')

# List collections and document counts
collections = db.list_collection_names()  # Get a list of collection names

# Check if there are any collections
if collections:
    st.write("Collections and their document counts:")
    for collection_name in collections:
        collection = db[collection_name]  # Access the collection
        count = collection.count_documents({})  # Count documents in the collection
        st.write(f"{collection_name}: {count} documents")
else:
    st.write("No collections found.")


# Select collectioon
collection_name = st.selectbox('Select a collection', collections)
collection = db[collection_name]  # Access the collection

# Select a document
st.write("Select a document")
documents = collection.find()
document_id = st.selectbox


# Example: Fetch all documents within the last week
from datetime import datetime, timedelta

# Calculate date one week ago
one_week_ago = datetime.utcnow() - timedelta(days=7)

# Query to fetch documents
documents = collection.find({'created_utc': {'$gte': one_week_ago}})

import pandas as pd

# Convert documents to DataFrame
df = pd.DataFrame(list(documents))

# Streamlit visualization
st.title('Bitcoin Subreddit Activity')

# Convert 'created_utc' to datetime
df['created_utc'] = pd.to_datetime(df['created_utc'])

# Simple line chart of scores over time
st.line_chart(df.set_index('created_utc')['score'])


# Assuming df is your DataFrame
# Convert 'created_utc' to datetime if not already
df['created_utc'] = pd.to_datetime(df['created_utc'])

# Sort by 'created_utc' to ensure correct cumulative calculation
df = df.sort_values(by='created_utc')

# Calculate cumulative max of 'num_comments' for each post
df['cumulative_max_comments'] = df.groupby('id')['num_comments'].cummax()



# Group by 'created_utc' day and sum 'cumulative_max_comments'
daily_comment_activity = df.resample('D', on='created_utc')['cumulative_max_comments'].sum().reset_index()

# Plotting with Streamlit
st.title('Cumulative Comment Activity Over Time')
st.line_chart(data=daily_comment_activity, x='created_utc', y='cumulative_max_comments')


# Ensure the DataFrame only contains the columns you want to display
df_display = df[['id', 'title', 'created_utc', 'num_comments','upvote_ratio','createdAt','sort_order','body']]

# Display the DataFrame as a table in Streamlit
st.dataframe(df_display)
