# 📘 University DB Projects – Spring 2025

Database Design course assignments  
**Sharif University of Technology**  
*Spring 2025*

This repository contains practical projects implemented for the **Database Design** course. Each project demonstrates hands-on use of database schema design, ORM-based query handling, and RESTful API implementation using Python and modern tools like SQLAlchemy, MongoDB, and Redis.

---

## 📁 Contents

- [`anime-api-orm/`](#-project-1-anime-api-with-orm) — ORM-based API to query anime data from a SQL dump
- [`research-papers-manager/`](#-project-2-research-papers-manager) — API system for managing research papers, citations, and caching (MongoDB + Redis)

---

## 📌 Project 1: Anime API with ORM

**Assignment Title:** implementing API with ORM  
**Language & Stack:** Python + FastAPI / Flask + SQLAlchemy (no raw SQL, no Django)  
**Focus:** ORM query implementation, API design, SQL schema interaction

### 🧾 Description

In this project, a pre-existing SQL dump is used to seed the database. An HTTP server is built to serve data using an ORM (SQLAlchemy) without using any raw SQL queries or high-level frameworks like Django. The application connects to a relational database and handles sessions manually.

### 📡 API Endpoints

> Each endpoint returns a JSON array of objects with keys mapped to DB columns.

#### `GET /anime/top`
Returns the 10 anime with the highest number of episodes.

#### `GET /users/top?page=1&offset=10&year=2017&gender=F`
Fetches female users who registered after 2017 and have an average rating above 8, with pagination.

#### `GET /users/:username/watched?count=10`
Lists the top 10 anime a specific user has watched, sorted by their personal rating (ascending).

#### `GET /anime/popular`
Returns the 3 most-watched anime genres based on user watch counts.

#### `GET /users/active/:year`
Fetches 5 users who spent the most days watching anime in a given year.

#### `GET /users/:username/similars`
Finds users with the most overlapping watched anime with a specific user.

#### `POST /anime/:anime_id/episodes?value=1`
Increases the episode count for a specific anime (defaults to +1 if no value provided).

### 🧪 Sample Response

```json
[
    {
        "user_id": 1,
        "username": "Alice",
        "age": 25,
        "email": "alice@example.com"
    },
    {
        "user_id": 2,
        "username": "Bob",
        "age": 30,
        "email": "bob@example.com"
    }
]
```

## 📌 Project 2: Research Papers Manager

**Assignment Title:** implementing API using MongoDB & Redis  
**Language & Stack:** Python + Flask + MongoDB + Redis  
**Focus:** NoSQL schema design, RESTful API implementation, caching, and real-time metrics

### 🧾 Description

This project implements a full-featured API system for managing university research papers. It uses MongoDB for persistent storage of user profiles, paper metadata, and citation relationships, and Redis for caching search results, tracking real-time view counts, and validating usernames during registration.

The system supports user registration and login, paper upload with metadata and citations, full-text search with relevance sorting, and real-time metrics for paper views. A background job periodically syncs Redis view counters back to MongoDB.

### 🗃️ Database Design

- **MongoDB Collections:**
  - `users`: stores user profiles with hashed passwords
  - `papers`: stores paper metadata and uploader reference
  - `citations`: stores citation relationships between papers

- **Redis Structures:**
  - `usernames` (hash): tracks taken usernames for instant validation
  - `search:<term>:<sort>:<order>` (string): caches search results for 5 minutes
  - `paper_views:<paper_id>` (string): tracks real-time view counts

### 📡 API Endpoints

#### `POST /signup`
Registers a new user with a unique username.  
Validates username availability via Redis.

#### `POST /login`
Authenticates a user and returns their user ID.

#### `POST /papers`
Uploads a new paper with metadata and optional citations.  
Requires `X-User-ID` header for authentication.

#### `GET /papers`
Searches papers by keyword, with optional sorting by relevance or publication date.  
Caches results in Redis for 5 minutes.

#### `GET /papers/<paper_id>`
Returns full paper details, citation count, and real-time view count.  
Increments view count in Redis.

### 🔁 Background Task

A scheduled job runs every 10 minutes using APScheduler to:

- Scan Redis for `paper_views:*` keys
- Sync view counts to MongoDB using `$inc`
- Reset Redis counters to zero

### 🧪 Sample Paper Document

```json
{
  "_id": "688f7ca99f9214ea0e99ff70",
  "title": "Government together between special eat daughter energy.",
  "authors": ["Timothy Gardner", "Robert Robertson", "Natalie Phillips"],
  "abstract": "Surface customer think...",
  "publication_date": "2024-08-29",
  "journal_conference": "Levine, Hernandez and Taylor",
  "keywords": ["them", "point", "different"],
  "uploaded_by": "688f7ca99f9214ea0e99ff25",
  "views": 0
}
```
### 🛠️ Tools & Libraries

- **Flask** – Lightweight web framework for building RESTful APIs
- **PyMongo** – MongoDB driver for Python to interact with document-based data
- **redis-py** – Redis client for caching and real-time metrics
- **bcrypt** – Secure password hashing for user authentication
- **Faker** – Used to generate realistic test data for papers and users
- **APScheduler** – Scheduler for background tasks like syncing Redis counters

### 📈 Features

- ⚡ Real-time view tracking using Redis counters
- 🧠 Cached search results for faster response times
- 🔗 Citation graph modeling between papers
- 🔄 Background sync of Redis metrics to MongoDB
- 🔐 Minimal session-based authentication with hashed passwords

### 🚧 Status

- ✅ Core endpoints implemented and tested
- ✅ Redis caching and view tracking integrated
- ✅ Background sync job operational
- 🧪 Final testing and performance tuning in progress

---

## 📎 License

This project is for educational use only and is part of coursework submitted to Sharif University of Technology.

---
