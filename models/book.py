from dataclasses import dataclass

@dataclass(frozen=True)
class Book:
    book_id: int
    isbn: str
    title: str
    author: str
    category: str
    year: int
    copies: int
