from datetime import datetime


def validate_paper_data(data):
    title = data.get('title', '').strip()
    authors = data.get('authors', [])
    abstract = data.get('abstract', '').strip()
    publication_date = data.get('publication_date', '').strip()
    journal_conference = data.get('journal_conference', '').strip()
    keywords = data.get('keywords', [])

    if not title or len(title) > 200:
        return False, "Title is required and must be at most 200 characters."

    if not isinstance(authors, list) or not (1 <= len(authors) <= 5):
        return False, "Authors must be a list of 1 to 5 names."

    for author in authors:
        if not isinstance(author, str) or len(author.strip()) > 100:
            return False, "Each author name must be a string up to 100 characters."

    if not abstract or len(abstract) > 1000:
        return False, "Abstract is required and must be at most 1000 characters."

    if publication_date:
        try:
            datetime.fromisoformat(publication_date)
        except ValueError:
            return False, "Publication date must be in valid ISO format (YYYY-MM-DD)."

    if journal_conference and len(journal_conference) > 200:
        return False, "Journal/Conference name must be at most 200 characters."

    if keywords:
        if not isinstance(keywords, list) or not (1 <= len(keywords) <= 5):
            return False, "Keywords must be a list of 1 to 5 strings."
        for kw in keywords:
            if not isinstance(kw, str) or len(kw.strip()) > 50:
                return False, "Each keyword must be a string up to 50 characters."

    return True, None
