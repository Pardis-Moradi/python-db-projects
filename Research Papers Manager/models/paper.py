from utils.db import db

papers_collection = db['papers']

"""
Papers document:
{
    _id: ObjectId,
    title: str,                   # required, max 200
    authors: [str],               # list of 1-5 names, max 100 each
    abstract: str,                # required, max 1000
    publication_date: datetime,   # ISODate
    journal_conference: str,      # optional, max 200
    keywords: [str],              # list of 1-5 words, max 50 each
    uploaded_by: ObjectId,        # reference to Users
    views: int                    # default 0, sync from Redis
}
"""