import re
from datetime import datetime

USERNAME_RE = re.compile(r'^[A-Za-z0-9_]{3,20}$')
EMAIL_RE    = re.compile(r'^[^@]+@[^@]+\.[^@]+$')
ISO_DATE_FMT = '%Y-%m-%d'

def validate_signup_input(data):
    errors = {}

    u = data.get("username", "")
    if not USERNAME_RE.match(u):
        errors["username"] = "3–20 chars; letters, digits, underscore."
    
    if not data.get("name") or len(data["name"]) > 100:
        errors["name"] = "Required; max 100 chars."
    
    e = data.get("email", "")
    if not EMAIL_RE.match(e) or len(e) > 100:
        errors["email"] = "Valid email; max 100 chars."
    
    pw = data.get("password", "")
    if len(pw) < 8:
        errors["password"] = "Min length 8."
    
    dept = data.get("department", "")
    if not dept or len(dept) > 100:
        errors["department"] = "Required; max 100 chars."
    
    return errors

def validate_login_input(data):
    errors = {}
    if not data.get("username"):
        errors["username"] = "Required."
    if not data.get("password"):
        errors["password"] = "Required."
    return errors

def validate_upload_paper_input(data):
    errors = {}
    if not data.get("title", "") or not (1 <= len(data.get("title", "")) <= 200):
        errors["title"] = "Invalid title."
    if not data.get("abstract", "") or not (1 <= len(data.get("abstract", "")) <= 1000):
        errors["abstract"] = "Invalid abstract."
    if data.get("journal_conference") and len(data.get("journal_conference", "")) > 200:
        errors["journal_conference"] = "Journal/Conference name too long."
    authors = data.get("authors", [])
    if not authors or not (1 <= len(authors) <= 5) or any(len(a) > 100 for a in authors):
        errors["authors"] = "Invalid authors section."
    keywords = data.get("keywords", [])
    if not keywords or not (1 <= len(keywords) <= 5) or any(len(k) > 50 for k in keywords):
        errors["keywords"] = "Invalid keywords section."
    try:
        _ = datetime.strptime(data.get("publication_date", ""), ISO_DATE_FMT)
    except Exception:
        errors["publication_date"] = "Invalid publication date."
    citations = data.get("citations", [])
    if citations and len(citations) > 5:
        errors["citations"] = "Max 5 citations allowed."
    return errors

def validate_search_papers_parameters(search_term, sort_by, order):
    errors = {}
    if not search_term:
        errors["search_term"] = "No search term given."
    if sort_by not in ('publication_date', 'relevance'):
        errors["sort_by"] = "Invalid sort_by param."
    if order not in ('asc', 'desc'):
        errors["order"] = "Invalid order param."
    return errors