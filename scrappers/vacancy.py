from datetime import datetime
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
    scrapped_at: datetime
    salary: Optional[str] = None
    published_at: Optional[str] = None
