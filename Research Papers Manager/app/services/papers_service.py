from pymongo.errors import DuplicateKeyError
from datetime import datetime
from bson import ObjectId

from ..extensions import mongo, redis_client, bcrypt

class InvalidUserID(Exception):
    pass

class InvalidCitationReference(Exception):
    pass

class PaperDoesntExist(Exception):
    pass

def add_paper(user_id, data):
    uid = ObjectId(user_id)
    if not user_id or not mongo.db.users.find_one({'_id': uid}):
        raise InvalidUserID
    
    citations = data.get('citations', [])
    for cite in citations:
        cid = ObjectId(cite)
        if not mongo.db.papers.find_one({'_id': cid}):
            raise InvalidCitationReference
        
    publication_date = datetime.strptime(data["publication_date"], '%Y-%m-%d')
        
    paper_doc = {
        "title":                data["title"],
        "authors":              data["authors"],
        "abstract":             data["abstract"],
        "publication_date":     publication_date,
        "journal_conference":   data["journal_conference"],
        "keywords":             data["keywords"],
        "uploaded_by":          user_id,
        "views":                0
    }

    try:
        result = mongo.db.papers.insert_one(paper_doc)
    except Exception:
        print("Exception in papers_service.add_paper()")

    for cid in citations:
        mongo.db.citations.insert_one({
            "paper_id": result.inserted_id,
            "cited_paper_id": cid
        })

    return result.inserted_id


def search_for_papers(search_term, sort_by, order):
    # Redis key
    redis_key = f"search:{search_term}:{sort_by}:{order}"
    cached = redis_client.get(redis_key)
    if cached:
        from json import loads
        return loads(cached)
    
    # Build MongoDB query
    mongo_query = {}
    sort = []
    if search_term:
        mongo_query["$text"] = {"$search": search_term}
        if sort_by == "relevance":
            sort = [("score", {"$meta": "textScore"})]
        else:
            sort = [("publication_date", 1 if order == "asc" else -1)]
    else:
        if sort_by == "relevance":
            # If no search term, default to publication_date
            sort_by = "publication_date"
        sort = [("publication_date", 1 if order == "asc" else -1)]

    # If sort by relevance, get textScore
    cursor = mongo.db.papers.find(mongo_query)
    if sort_by == "relevance" and search_term:
        cursor = cursor.sort([("score", {"$meta": "textScore"})])
    else:
        cursor = cursor.sort(sort)

    # Only project needed fields
    fields = {"title":1, "authors":1, "publication_date":1, "journal_conference":1, "keywords":1}
    papers = []
    for doc in cursor:
        papers.append({
            "id": str(doc["_id"]),
            "title": doc.get("title", ""),
            "authors": doc.get("authors", []),
            "publication_date": doc.get("publication_date").strftime('%Y-%m-%d') if doc.get("publication_date") else "",
            "journal_conference": doc.get("journal_conference", ""),
            "keywords": doc.get("keywords", [])
        })

    # Cache results in Redis for 5 minutes (300s)
    from json import dumps
    redis_client.setex(redis_key, 300, dumps(papers))

    return papers

def get_paper_details(paper_id):
    # Validate paper_id format
    pid = ObjectId(paper_id)
    paper = mongo.db.papers.find_one({'_id':pid})
    if not paper:
        raise PaperDoesntExist

    # Count citations
    citation_count = mongo.db.citations.count_documents({"cited_paper_id": pid})

    # Increment and get views from Redis
    redis_key = f"paper_views:{paper_id}"
    redis_client.incr(redis_key)
    views = redis_client.get(redis_key)
    views = int(views) if views else 0

    # Prepare response
    response = {
        "id": paper_id,
        "title": paper.get("title", ""),
        "authors": paper.get("authors", []),
        "abstract": paper.get("abstract", ""),
        "publication_date": paper.get("publication_date").strftime('%Y-%m-%d') if paper.get("publication_date") else "",
        "journal_conference": paper.get("journal_conference", ""),
        "keywords": paper.get("keywords", []),
        "citation_count": citation_count,
        "views": views
    }

    return response