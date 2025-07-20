from bson import ObjectId


def validate_citation_data(data):
    paper_id = data.get('paper_id')
    cited_paper_id = data.get('cited_paper_id')

    if not paper_id or not ObjectId.is_valid(paper_id):
        return False, "Invalid paper_id."

    if not cited_paper_id or not ObjectId.is_valid(cited_paper_id):
        return False, "Invalid cited_paper_id."

    if paper_id == cited_paper_id:
        return False, "A paper cannot cite itself."

    return True, None
