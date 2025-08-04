# scripts/init_db.py

import os
from dotenv import load_dotenv
from pymongo import MongoClient, ASCENDING, TEXT

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client.get_default_database()

# 1. Users: unique index on username
db.users.create_index(
    [("username", ASCENDING)], 
    unique=True,
    name="idx_users_username"
)

# 2. Papers: text index on title, abstract, keywords
db.papers.create_index(
    [("title", TEXT), ("abstract", TEXT), ("keywords", TEXT)],
    name="idx_papers_text"
)

# 3. Citations: index on cited_paper_id
db.citations.create_index(
    [("cited_paper_id", ASCENDING)],
    name="idx_citations_cited_paper"
)

print("✔️  MongoDB indexes created successfully.")

