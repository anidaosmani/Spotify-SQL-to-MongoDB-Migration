import pyodbc
from pymongo import MongoClient

print("===== VALIDATION REPORT =====\n")

# -------------------------
# CONNECT TO SQL SERVER
# -------------------------

sql_conn = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=DESKTOP-C5SNIP3;"
    "DATABASE=SpotifyDB;"
    "Trusted_Connection=yes;"
)

sql_cursor = sql_conn.cursor()

# -------------------------
# CONNECT TO MONGODB
# -------------------------

mongo_client = MongoClient("mongodb://localhost:27017")

mongo_db = mongo_client["SpotifyMongo"]
tracks_collection = mongo_db["tracks"]

# -------------------------
# VALIDATION 1
# RECORD COUNTS
# -------------------------

sql_cursor.execute("SELECT COUNT(*) FROM Tracks")
sql_tracks = sql_cursor.fetchone()[0]

mongo_tracks = tracks_collection.count_documents({})

print("TRACK COUNTS")
print("SQL Tracks:", sql_tracks)
print("Mongo Tracks:", mongo_tracks)

if sql_tracks == mongo_tracks:
    print("PASS\n")
else:
    print("FAIL\n")

# -------------------------
# VALIDATION 2
# CHECKSUM VALIDATION
# -------------------------

sql_cursor.execute("""
SELECT
    COUNT(*) AS total_tracks,
    MIN(track_id) AS min_track,
    MAX(track_id) AS max_track
FROM Tracks
""")

sql_result = sql_cursor.fetchone()

mongo_count = tracks_collection.count_documents({})

mongo_min_doc = tracks_collection.find_one(
    sort=[("track_id", 1)]
)

mongo_max_doc = tracks_collection.find_one(
    sort=[("track_id", -1)]
)

mongo_min = mongo_min_doc["track_id"]
mongo_max = mongo_max_doc["track_id"]

print("CHECKSUM VALIDATION")
print("SQL Count:", sql_result[0])
print("Mongo Count:", mongo_count)

print("SQL Min Track ID:", sql_result[1])
print("Mongo Min Track ID:", mongo_min)

print("SQL Max Track ID:", sql_result[2])
print("Mongo Max Track ID:", mongo_max)

if sql_result[0] == mongo_count:
    print("PASS\n")
else:
    print("FAIL\n")

# -------------------------
# VALIDATION 3
# POPULARITY CHECK
# -------------------------

sql_cursor.execute("""
SELECT COUNT(*)
FROM Tracks
WHERE popularity >= 70
""")

sql_popular = sql_cursor.fetchone()[0]

mongo_popular = tracks_collection.count_documents(
    {"popularity_category": "High"}
)

print("POPULARITY CHECK")
print("SQL Popular Tracks:", sql_popular)
print("Mongo High Popularity:", mongo_popular)

if sql_popular == mongo_popular:
    print("PASS\n")
else:
    print("FAIL\n")

# -------------------------
# VALIDATION 4
# SPOT CHECK
# -------------------------

sql_cursor.execute("""
SELECT TOP 1 track_name
FROM Tracks
ORDER BY track_name
""")

sample_track = sql_cursor.fetchone()[0]

mongo_track = tracks_collection.find_one(
    {"track_name": sample_track}
)

print("SPOT CHECK")
print("Track:", sample_track)

if mongo_track:
    print("PASS\n")
else:
    print("FAIL\n")

print("===== VALIDATION FINISHED =====")