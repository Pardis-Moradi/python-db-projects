from utils.db import db

citations_collection = db['citations']

"""
Citations document:
{
    _id: ObjectId,
    paper_id: ObjectId,         # paper that is citing another paper
    cited_paper_id: ObjectId    # paper that is being cited
}
"""
