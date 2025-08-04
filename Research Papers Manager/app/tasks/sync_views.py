import re
import logging
from app import mongo, redis_client
from bson import ObjectId

logger = logging.getLogger(__name__)
PATTERN = re.compile(r"^paper_views:(?P<pid>.+)$")

def sync_views_job():
    """
    Scans Redis for paper_views keys, syncs counts to MongoDB,
    and resets the Redis counter to zero.
    """
    # Use SCAN to avoid blocking Redis
    cursor = 0
    while True:
        cursor, keys = redis_client.scan(cursor, match="paper_views:*", count=100)
        for key in keys:
            key = key.decode() if isinstance(key, bytes) else key
            match = PATTERN.match(key)
            if not match:
                continue

            paper_id = match.group("pid")
            try:
                # GET current counter
                count = int(redis_client.get(key) or 0)
                if count > 0:
                    # Persist into Mongo: increment the views field
                    mongo.db.papers.update_one(
                        {"_id": ObjectId(paper_id)},
                        {"$inc": {"views": count}}
                    )
                    logger.info(f"Synced {count} views for paper {paper_id}")

                # Reset Redis counter
                redis_client.set(key, 0)
            except Exception as e:
                logger.exception(f"Error syncing views for {paper_id}: {e}")

        if cursor == 0:
            break
