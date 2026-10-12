from dataclasses import dataclass

@dataclass(frozen=True)
class Member:
    member_id: int
    member_code: str
    name: str
    email: str
    phone: str
