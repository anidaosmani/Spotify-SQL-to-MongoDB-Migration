import pyodbc
from pymongo import MongoClient

# ==========================
# SQL SERVER CONNECTION
# ==========================

sql_conn = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=DESKTOP-C5SNIP3;"
    "DATABASE=SpotifyDB;"
    "Trusted_Connection=yes;"
)

sql_cursor = sql_conn.cursor()

# ==========================
# MONGODB CONNECTION
# ==========================

mongo_client = MongoClient("mongodb://localhost:27017")

mongo_db = mongo_client["SpotifyMongo"]
tracks_collection = mongo_db["tracks"]

# ==========================
# IDEMPOTENT MIGRATION
# ==========================

tracks_collection.delete_many({})

# ==========================
# READ DATA FROM SQL SERVER
# ==========================

sql_cursor.execute("""
SELECT
    t.track_id,
    t.track_name,
    t.duration_ms,
    t.popularity,
    t.explicit,

    a.artist_name,
    al.album_name,
    g.genre_name,

    af.danceability,
    af.energy,
    af.valence,
    af.tempo,
    af.acousticness,
    af.instrumentalness,
    af.liveness,
    af.speechiness

FROM Tracks t
JOIN Artists a
    ON t.artist_id = a.artist_id

JOIN Albums al
    ON t.album_id = al.album_id

JOIN Genres g
    ON t.genre_id = g.genre_id

JOIN AudioFeatures af
    ON t.track_id = af.track_id
""")

rows = sql_cursor.fetchall()

print("Rows fetched from SQL:", len(rows))

# ==========================
# MIGRATION
# ==========================

count = 0

for row in rows:

    # ----------------------
    # DERIVED FIELD 1
    # ----------------------

    duration_minutes = round(row.duration_ms / 60000, 2)

    # ----------------------
    # DERIVED FIELD 2
    # ----------------------

    if row.popularity >= 70:
        popularity_category = "High"
    elif row.popularity >= 40:
        popularity_category = "Medium"
    else:
        popularity_category = "Low"

    # ----------------------
    # DERIVED FIELD 3
    # ----------------------

    if row.energy >= 0.7:
        energy_level = "High"
    elif row.energy >= 0.4:
        energy_level = "Medium"
    else:
        energy_level = "Low"

    # ----------------------
    # DERIVED FIELD 4
    # ----------------------

    mood = "Happy" if row.valence >= 0.5 else "Sad"

    document = {
        "track_id": row.track_id,
        "track_name": row.track_name,
        "duration_ms": row.duration_ms,
        "explicit": bool(row.explicit),

        "artist": {
            "name": row.artist_name
        },

        "album": {
            "name": row.album_name
        },

        "genre": row.genre_name,

        "duration_minutes": duration_minutes,
        "popularity_category": popularity_category,
        "energy_level": energy_level,
        "mood": mood,

        "audio_features": {
            "danceability": row.danceability,
            "energy": row.energy,
            "valence": row.valence,
            "tempo": row.tempo,
            "acousticness": row.acousticness,
            "instrumentalness": row.instrumentalness,
            "liveness": row.liveness,
            "speechiness": row.speechiness
        }
    }

    tracks_collection.insert_one(document)

    count += 1

    if count % 1000 == 0:
        print(f"{count} documents migrated")

print("\nMigration completed!")
print("Total documents inserted:", count)

# ==========================
# VERIFY
# ==========================

print(
    "Documents currently in MongoDB:",
    tracks_collection.count_documents({})
)