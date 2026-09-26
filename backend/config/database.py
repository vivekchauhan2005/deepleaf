from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise Exception("MONGO_URI not found in .env file")

client = MongoClient(MONGO_URI)

db = client["deepleaf"]

print("✅ MongoDB Connected Successfully")