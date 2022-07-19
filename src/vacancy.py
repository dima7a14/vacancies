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
    published_at: datetime
    salary: Optional[str] = None

    def __eq__(self, obj: object) -> bool:
        return self.link == obj.link

    def render_markdown(self) -> str:
        output: str = f"""
            **[{self.title}]({self.link})**\n
            {self.detail}\n
        """

        if self.salary is not None:
            output += f"**Salary: **{self.salary}\n"

        output += f"""
            **Locations: **{", ".join(self.locations)}
            **Company: **{self.company}
            **Origin: **{self.origin}
            **Published at: **{self.published_at}
        """

        return output


def parse_vacancy(data: dict) -> Vacancy:
    return Vacancy(
        title=data.get("title", ""),
        detail=data.get("detail", ""),
        company=data.get("company", ""),
        link=data.get("link", ""),
        locations=data.get("locations", []),
        origin=data.get("origin", ""),
        published_at=datetime.fromisoformat(data.get("published_at")),
        salary=data.get("salary", ""),
        scrapped_at=datetime.fromisoformat(data.get("scrapped_at")),
    )
