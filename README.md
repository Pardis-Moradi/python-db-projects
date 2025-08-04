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
**Status:** _Coming soon_  
**Stack:** Python + MongoDB + Redis  
**Focus:** API design, document DB modeling, caching, and performance optimization

> Detailed project description and implementation to be added soon.

---

## 📎 License

This project is for educational use only and is part of coursework submitted to Sharif University of Technology.

---
