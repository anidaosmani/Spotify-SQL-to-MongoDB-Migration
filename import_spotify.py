import pandas as pd
import pyodbc

df = pd.read_csv("../data/dataset.csv")

conn = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=DESKTOP-C5SNIP3;"
    "DATABASE=SpotifyDB;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()

# Existing tracks
cursor.execute("SELECT track_id FROM Tracks")
valid_tracks = set(row.track_id for row in cursor.fetchall())

inserted = 0

for _, row in df.iterrows():

    track_id = str(row["track_id"])

    if track_id not in valid_tracks:
        continue

    try:
        cursor.execute("""
        INSERT INTO AudioFeatures
        (
            track_id,
            danceability,
            energy,
            valence,
            tempo,
            acousticness,
            instrumentalness,
            liveness,
            speechiness
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        track_id,
        float(row["danceability"]),
        float(row["energy"]),
        float(row["valence"]),
        float(row["tempo"]),
        float(row["acousticness"]),
        float(row["instrumentalness"]),
        float(row["liveness"]),
        float(row["speechiness"])
        )

        inserted += 1

        if inserted % 1000 == 0:
            print(f"{inserted} features inserted")

    except:
        pass

conn.commit()

print("AudioFeatures inserted:", inserted)