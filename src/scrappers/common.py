from typing import Protocol
from dataclasses import dataclass
from enum import Enum
import requests
from ..vacancy import Vacancy


class Specialization(Enum):
    FRONTEND = "frontend"
    NODEJS = "node.js"
    PYTHON = "python"
    FLUTTER = "flutter"


class Location(Enum):
    REMOTE = "remote"
    PART_TIME = "part-time"
    UKRAINE = "ukraine"

class Scrapper(Protocol):
    def __init__(self, specializations: list[Specialization], locations: list[Location]) -> None:
        ...

    def scrape() -> list[Vacancy]:
        ...


class ScrapperService:
    scrappers: list[Scrapper] = []
    vacancies: list[Vacancy] = []

    def register(self, scrapper: Scrapper) -> None:
        self.scrappers.append(scrapper)

    def run(self) -> None:
        for scrapper in self.scrappers:
            scrapped_vacancies = scrapper.scrape()

            for scrapped_vacancy in scrapped_vacancies:
                if scrapped_vacancy not in self.vacancies:
                    self.vacancies.extend(scrapper.scrape())


@dataclass
class ScrapperSelectors:
    vacancy: dict[str, str]
    vacancy_link: dict[str, str]
    vacancy_title: dict[str, str]
    vacancy_salary: dict[str, str]
    vacancy_locations: dict[str, str]
    vacancy_detail: dict[str, str]
    vacancy_published_at: dict[str, str]
    vacancy_company:dict[str, str]
    vacancy_more: dict[str, str]


def get_resource(url: str, params: dict = None) -> requests.Response:
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
        "Accept-Language": "en-US",
    }
    response = requests.get(url=url, headers=headers, params=params)

    return response
