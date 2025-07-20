from utils.cache import redis_client


def is_username_taken(username):
    """
    Checks if username already exists in Redis hash.
    """
    return redis_client.hexists('usernames', username)


def mark_username_taken(username):
    """
    Marks username as taken in Redis hash.
    """
    redis_client.hset('usernames', username, 1)
