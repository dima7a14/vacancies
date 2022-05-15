from dataclasses import dataclass
from typing import Optional


@dataclass
class Vacancy:
    title: str
    detail: str
    link: str
    company: str
    origin: str
    locations: list[str]
    salary: Optional[str] = None
    published_at: Optional[str] = None
