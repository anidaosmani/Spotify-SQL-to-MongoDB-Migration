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

## Dataset

**Dataset:** Spotify Tracks Dataset

The dataset contains approximately 114,000 Spotify tracks with information about:

* Tracks
* Artists
* Albums
* Genres
* Audio Features

## Relational Database Schema

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

## Data Population Results

* Artists: 31,281
* Genres: 114
* Albums: 45,828
* Tracks: 84,975
* Audio Features: 84,975

## MongoDB Data Model

**Database:** SpotifyMongo

**Collection:** tracks

## Derived Fields Created During Migration

### duration_minutes

Track duration converted from milliseconds to minutes.

### popularity_category

* High
* Medium
* Low

### energy_level

* High
* Medium
* Low

### mood

* Happy
* Sad

## Running the Migration

```bash
cd migration
python migrate_to_mongo.py
```

## Running Validation

```bash
cd validation
python validate_migration.py
```

Validation checks include:

* Record count comparison
* Checksum validation
* Popularity category validation
* Spot-check validation

## Power BI Dashboard

1. Popularity Category Distribution
2. Energy Level Distribution
3. Average Track Duration by Genre

## Conclusion

This project successfully demonstrates the migration of Spotify music data from Microsoft SQL Server to MongoDB.

The migration process included data transformation, validation, and visualization, providing a complete ETL workflow and highlighting the differences between relational and NoSQL database systems.
