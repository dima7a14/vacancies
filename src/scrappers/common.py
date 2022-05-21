from typing import Protocol
from dataclasses import dataclass
import requests
from ..vacancy import Vacancy


class Scrapper(Protocol):
    def scrape() -> list[Vacancy]:
        ...


class ScrapperService:
    scrappers: list[Scrapper] = []
    vacancies: list[Vacancy] = []

    def register(self, scrapper: Scrapper) -> None:
        self.scrappers.append(scrapper)

    def run(self) -> None:
        for scrapper in self.scrappers:
            self.vacancies.extend(scrapper.scrape())


@dataclass
class ScrapperSelectors:
    vacancy_selector: str
    vacancy_link_selector: str
    vacancy_title_selector: str
    vacancy_salary_selector: str
    vacancy_locations_selector: str
    vacancy_detail_selector: str
    vacancy_published_at_selector: str
    vacancy_company_selector:str
    vacancy_more_selector: str


def get_resource(url: str, params: dict = None) -> requests.Response:
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
    }
    response = requests.get(url=url, headers=headers, params=params)

    return response
