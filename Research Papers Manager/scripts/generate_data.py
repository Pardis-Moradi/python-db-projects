# scripts/generate_data.py

import os
import re
import random
from datetime import datetime, date, time
from dotenv import load_dotenv
from faker import Faker
from pymongo import MongoClient
from redis import Redis
import bcrypt

# Load environment variables
load_dotenv()
MONGO_URI   = os.getenv("MONGO_URI")
REDIS_URL   = os.getenv("REDIS_URL")

# Initialize clients
fake         = Faker()
mongo_client = MongoClient(MONGO_URI)
db           = mongo_client.get_default_database()
redis_client = Redis.from_url(REDIS_URL)

# Regex for valid username: 3–20 chars, letters, digits, underscore
USERNAME_RE = re.compile(r'^[A-Za-z0-9_]{3,20}$')

def make_username(existing):
    while True:
        u = fake.user_name()
        if USERNAME_RE.match(u) and u not in existing:
            return u

def make_password():
    # random length between 8 and 12; include letters & digits
    length = random.randint(8, 12)
    pw = fake.password(length=length, special_chars=False, digits=True, upper_case=True, lower_case=True)
    return pw

def random_date(start: date, end: date) -> date:
    return fake.date_between_dates(date_start=start, date_end=end)

def main():
    # --- Generate Users ---
    users, usernames = [], set()
    for _ in range(100):
        username   = make_username(usernames)
        usernames.add(username)

        raw_pw     = make_password()
        hashed_pw  = bcrypt.hashpw(raw_pw.encode(), bcrypt.gensalt()).decode()

        users.append({
            "username":   username,
            "name":       fake.name()[:100],
            "email":      fake.unique.email()[:100],
            "password":   hashed_pw,
            "department": fake.word()[:100]
        })

    res = db.users.insert_many(users)
    user_ids = res.inserted_ids
    print(f"Inserted {len(user_ids)} users.")

    # Sync usernames into Redis
    for u in usernames:
        redis_client.hset("usernames", u, 1)
    print("Synced usernames to Redis hash.")

    # --- Generate Papers ---
    papers = []
    date_start = datetime(2015, 6, 5, 0, 0, 0)
    date_end   = datetime(2025, 6, 5, 0, 0, 0)

    for _ in range(1000):
        date_only = fake.date_between_dates(date_start=date_start,
                                        date_end=date_end)
        pub_date = datetime.combine(date_only,
                                       time.min)
        authors  = [fake.name()[:100] for __ in range(random.randint(1, 5))]
        keywords = fake.words(nb=random.randint(1, 5))
        keywords = [kw[:50] for kw in keywords]

        papers.append({
            "title":               fake.sentence(nb_words=random.randint(6, 10))[:200],
            "authors":             authors,
            "abstract":            fake.paragraph(nb_sentences=5)[:1000],
            "publication_date":    pub_date,
            "journal_conference":  fake.company()[:200],
            "keywords":            keywords,
            "uploaded_by":         random.choice(user_ids),
            "views":               0
        })

    res = db.papers.insert_many(papers)
    paper_ids = res.inserted_ids
    print(f"Inserted {len(paper_ids)} papers.")

    # --- Generate Citations ---
    citations = []
    for pid in paper_ids:
        # choose 0-5 other papers, no self-citation
        others = [x for x in paper_ids if x != pid]
        cited = random.sample(others, k=random.randint(0, 5))
        for c in cited:
            citations.append({
                "paper_id":        pid,
                "cited_paper_id":  c
            })

    if citations:
        db.citations.insert_many(citations)
    print(f"Inserted {len(citations)} citations.")

if __name__ == "__main__":
    main()

