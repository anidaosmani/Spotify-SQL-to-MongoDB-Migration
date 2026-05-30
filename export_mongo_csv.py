from pymongo import MongoClient
import pandas as pd

client = MongoClient("mongodb://localhost:27017")

db = client["SpotifyMongo"]

docs = list(db["tracks"].find({}, {"_id": 0}))

df = pd.json_normalize(docs)

df.to_csv("spotify_mongo_export.csv", index=False)

print("CSV exported successfully!")