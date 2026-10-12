from services.book_service import search_books


def search_before_add(term):
    return search_books(term)
