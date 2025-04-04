from pymongo import MongoClient

MONGO_URL = "mongodb+srv://saiyad:uoJOu66jNcxhvXuh@cluster0.jszmm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

try:
    client = MongoClient(MONGO_URL)
    db = client.hotelmind
    hotels_collection = db.hotels
    print("✅ MongoDB Connected Successfully!")
except Exception as e:
    print("❌ MongoDB Connection Failed")
    print(e)
