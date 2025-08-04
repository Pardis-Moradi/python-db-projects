from pymongo.errors import DuplicateKeyError
from ..extensions import mongo, redis_client, bcrypt

class UserAlreadyExists(Exception):
    pass

class InvalidCredentials(Exception):
    pass

def register_user(data):
    username = data["username"]
    # 1) Check Redis for existing username
    if redis_client.hexists("usernames", username):
        raise UserAlreadyExists()

    # 2) Hash password
    hashed = bcrypt.generate_password_hash(
        data["password"].encode()
    ).decode()

    user_doc = {
        "username":   username,
        "name":       data["name"],
        "email":      data["email"],
        "password":   hashed,
        "department": data["department"]
    }

    # 3) Insert into MongoDB
    try:
        result = mongo.db.users.insert_one(user_doc)
    except DuplicateKeyError:
        # race condition or direct Mongo duplicate
        raise UserAlreadyExists()

    # 4) Mark username taken in Redis
    redis_client.hset("usernames", username, 1)
    return result.inserted_id

def authenticate_user(data):
    user = mongo.db.users.find_one({"username": data["username"]})
    if not user:
        raise InvalidCredentials()

    # bcrypt check
    if not bcrypt.check_password_hash(
        user["password"], data["password"]
    ):
        raise InvalidCredentials()

    return user["_id"]

