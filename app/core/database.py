import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load the API keys from your .env walk-in cooler
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

def get_database():
    """Establishes the secure connection to the NMM MongoDB Data House."""
    if not MONGO_URI:
        raise ValueError("Security Alert: MONGO_URI is missing from the .env file.")
    
    # Connect to the MongoDB cluster
    client = MongoClient(MONGO_URI)
    
    # Return the specific database for our agents
    return client["nmm_palzani_db"]

if __name__ == "__main__":
    db = get_database()
    print("MongoDB Data House connection successful!")
