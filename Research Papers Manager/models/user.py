from utils.db import db

users_collection = db['users']

"""
Users document:
{
    _id: ObjectId,
    username: str,     # unique, 3-20 chars
    name: str,         # max 100
    email: str,        # max 100, valid email
    password: str,     # bcrypt hash
    department: str    # max 100
}
"""