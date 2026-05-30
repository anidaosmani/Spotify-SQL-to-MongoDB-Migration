# Spotify Music Data Migration: SQL Server to MongoDB

## Project Overview

This project demonstrates the migration of Spotify music data from a relational database (Microsoft SQL Server) to a NoSQL database (MongoDB).

The project includes:

* Relational database design and implementation
* Data population from the Spotify Tracks Dataset
* Data migration from SQL Server to MongoDB
* Data transformation during migration
* Automated validation checks
* Data visualization using Power BI

The objective is to compare relational and non-relational database systems and demonstrate an end-to-end ETL (Extract, Transform, Load) pipeline.

---

## Technologies Used

### Relational Database

* Microsoft SQL Server
* SQL Server Management Studio (SSMS)

### NoSQL Database

* MongoDB
* MongoDB Compass

### Programming Language

* Python 3

### Python Libraries

* pandas
* pyodbc
* pymongo

### Visualization

* Power BI Desktop

### Version Control

* GitHub

---

## Dataset

Dataset: Spotify Tracks Dataset

The dataset contains approximately 114,000 Spotify tracks with information about:

* Tracks
* Artists
* Albums
* Genres
* Audio Features

---

## Relational Database Schema

The SQL Server database contains the following tables:

### Artists

* artist_id (PK)
* artist_name
* followers
* popularity

### Genres

* genre_id (PK)
* genre_name

### Albums

* album_id (PK)
* album_name
* release_date
* artist_id (FK)

### Tracks

* track_id (PK)
* track_name
* duration_ms
* popularity
* explicit
* artist_id (FK)
* album_id (FK)
* genre_id (FK)

### AudioFeatures

* feature_id (PK)
* track_id (FK)
* danceability
* energy
* valence
* tempo
* acousticness
* instrumentalness
* liveness
* speechiness

---

## Data Population Results

The database was populated with:

* Artists: 31,281
* Genres: 114
* Albums: 45,828
* Tracks: 84,975
* Audio Features: 84,975

---

## MongoDB Data Model

Database:

SpotifyMongo

Collection:

tracks

Example document structure:

```json
{
  "track_id": "...",
  "track_name": "...",
  "artist": {
    "name": "..."
  },
  "album": {
    "name": "..."
  },
  "genre": "...",
  "duration_minutes": 3.54,
  "popularity_category": "Medium",
  "energy_level": "High",
  "mood": "Happy",
  "audio_features": {
    "danceability": 0.72,
    "energy": 0.85,
    "valence": 0.68
  }
}
```

---

## Derived Fields Created During Migration

The following fields were generated during migration:

### duration_minutes

Track duration converted from milliseconds to minutes.

### popularity_category

Popularity score converted into:

* High
* Medium
* Low

### energy_level

Energy value converted into:

* High
* Medium
* Low

### mood

Generated from valence values:

* Happy
* Sad

---

## Running the Migration

Navigate to the migration folder:

```bash
cd migration
```

Run:

```bash
python migrate_to_mongo.py
```

The script:

* Reads data from SQL Server
* Creates derived fields
* Migrates data into MongoDB
* Clears old MongoDB documents before migration to ensure idempotency

---

## Running Validation

Navigate to:

```bash
cd validation
```

Run:

```bash
python validate_migration.py
```

Validation checks include:

* Record count comparison
* Popularity category validation
* Spot-check validation

---

## Power BI Dashboard

The Power BI dashboard contains:

1. Popularity Category Distribution
2. Energy Level Distribution
3. Average Track Duration by Genre

The dashboard uses data exported from MongoDB.

---

## Project Structure

```text
SpotifyProject
│
├── data
│   └── dataset.csv
│
├── sql
│   └── import_spotify.py
│
├── migration
│   ├── migrate_to_mongo.py
│   └── export_mongo_csv.py
│
├── validation
│   └── validate_migration.py
│
├── screenshots
│
├── powerbi
│   └── SpotifyDashboard.pbix
│
└── README.md
```

---

## Conclusion

This project successfully demonstrates the migration of Spotify music data from Microsoft SQL Server to MongoDB.

The migration process included data transformation, validation, and visualization, providing a complete ETL workflow and highlighting the differences between relational and NoSQL database systems.
