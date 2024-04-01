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
