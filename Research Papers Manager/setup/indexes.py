from models.user import users_collection
from models.paper import papers_collection
from models.citation import citations_collection


def create_user_indexes():
    users_collection.create_index(
        [('username', 1)],
        unique=True,
        name='unique_username_index'
    )


def create_paper_indexes():
    papers_collection.create_index([
            ('title', 'text'),
            ('abstract', 'text'),
            ('keywords', 'text')
        ],
        name='papers_text_search_index'
    )


def create_citation_indexes():
    citations_collection.create_index(
        [('cited_paper_id', 1)],
        name='cited_paper_id_index'
    )


def create_all_indexes():
    """
    Call this function at app startup to ensure all necessary indexes exist.
    """
    create_user_indexes()
    create_paper_indexes()
    create_citation_indexes()
