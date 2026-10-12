from dataclasses import dataclass

@dataclass(frozen=True)
class Issue:
    issue_id: int
    book_id: int
    member_id: int
    issue_date: str
    return_date: str | None
    status: str
