from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum

from bs4 import BeautifulSoup, Tag
import dateparser

from .common import get_resource, Specialization, Location
from ..vacancy import Vacancy


class DouCategory(Enum):
    FRONTEND = "Front End"
    FLUTTER = "Flutter"
    NODEJS = "Node.js"
    PYTHON = "Python"


class DouLocation(Enum):
    REMOTE = "remote"


@dataclass
class DouScrapper:
    main_url: str = field(init=False, default="https://jobs.dou.ua/vacancies/")
    selectors: dict[str, dict[str, str]] = field(init=False, default_factory=lambda: {
        "vacancy": {"class_": "vacancy"},
        "vacancy_link": {"class_": "vt"},
        "vacancy_title": {"class_": "vt"},
        "vacancy_published_at": {"class_": "date"},
        "vacancy_salary": {"class_": "salary"},
        "vacancy_locations": {"class_": "cities"},
        "vacancy_detail": {"class_": "sh-info"},
        "vacancy_company": {"class_": "company"},
        "vacancy_more": {"class_": "more-btn"},
    })
    category: str = field()
    location: str = field()

    def parse_vacancy_html(self, vacancy_html: Tag) -> Vacancy:
        link = vacancy_html.find(**self.selectors["vacancy_link"]).get("href")

        title = vacancy_html.find(**self.selectors["vacancy_title"])

        if title is not None:
            title = title.get_text(strip=True)

        published_at = vacancy_html.find(**self.selectors["vacancy_published_at"])

        if published_at is not None:
            published_at = dateparser.parse(published_at.get_text(strip=True))
        else:
            published_at = datetime.now()

        salary = vacancy_html.find(**self.selectors["vacancy_salary"])

        if salary is not None:
            salary = salary.get_text(strip=True)

        locations = vacancy_html.find(**self.selectors["vacancy_locations"])

        if locations is not None:
            locations = locations.get_text(strip=True).split(", ")
        else:
            locations = []

        detail = vacancy_html.find(**self.selectors["vacancy_detail"])

        if detail is not None:
            detail = detail.get_text(strip=True)

        company = vacancy_html.find(**self.selectors["vacancy_company"])

        if company is not None:
            company = company.get_text(strip=True)

        vacancy = Vacancy(
            title=title,
            detail=detail,
            link=link,
            company=company,
            locations=locations,
            origin="DOU",
            published_at=published_at,
            salary=salary,
            scrapped_at=datetime.now(),
        )

        return vacancy

    def scrape(self) -> list[Vacancy]:
        try:
            resource = get_resource(self.main_url, params={"remote": self.location, "category": self.category})
            soup = BeautifulSoup(resource.content, "html.parser")
            nodes = soup.find_all("div", **self.selectors["vacancy"])
            vacancies = [self.parse_vacancy_html(node) for node in nodes]

            return vacancies
        except Exception as e:
            print(e)
            return []


def make_dou_scrappers(specializations: list[Specialization], locations: list[Location]) -> list[DouScrapper]:
    dou_categories: list[DouCategory] = []
    dou_locations: list[DouLocation] = []

    for specialization in specializations:
        match specialization:
            case Specialization.FRONTEND.value:
                dou_categories.append(DouCategory.FRONTEND)
            case Specialization.NODEJS.value:
                dou_categories.append(DouCategory.NODEJS)
            case Specialization.PYTHON.value:
                dou_categories.append(DouCategory.PYTHON)
            case Specialization.FLUTTER.value:
                dou_categories.append(DouCategory.FLUTTER)
            case _:
                print(f"There is no match for specialization {specialization} in DouScrapper")

    for location in locations:
        match location:
            case Location.REMOTE.value:
                dou_locations.append(DouLocation.REMOTE)
            case _:
                print(f"There is no match for location {location} in DouScrapper")

    scrappers: list[DouScrapper] = []

    for category in dou_categories:
        for location in dou_locations:
            scrappers.append(DouScrapper(category.value, location.value))
    
    return scrappers