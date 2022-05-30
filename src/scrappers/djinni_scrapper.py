from typing import Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field

from bs4 import BeautifulSoup, Tag
import dateparser

from .common import get_resource
from ..vacancy import Vacancy

@dataclass
class DjinniScrapper:
    main_url: str = field(init=False, default="https://djinni.co/jobs/")
    selectors: dict[str, dict[str, str]] = field(init=False, default_factory=lambda: {
        "vacancy": {"class_": "list-jobs__item"},
        "vacancy_link": {"class_": "profile"},
        "vacancy_title": {"class_": "profile"},
        "vacancy_published_at": {"class_": "text-date"},
        "vacancy_salary": {"class_": "public-salary-item"},
        "vacancy_detail": {"class_": "list-jobs__description"},
        "vacancy_locations": {"class_": "icon-home_work"},
        "vacancy_company": {"class_": "list-jobs__details__info"},
    })
    development: str = field()
    employment: str = field()
    salary: Optional[int] = field(default=None)

    @staticmethod
    def _parse_published_at(published_at: str) -> str:
        if published_at == "сьогодні":
            return datetime.now()
        
        if published_at == "вчора":
            return datetime.now() - timedelta(days=1)

        return dateparser.parse(published_at)

    def parse_vacancy_html(self, vacancy_html: Tag) -> Vacancy:
        link = self.main_url[:-6] + vacancy_html.find("a", **self.selectors["vacancy_link"]).get("href")

        title = vacancy_html.find(**self.selectors["vacancy_title"])

        if title is not None:
            title = title.get_text(strip=True)

        published_at = vacancy_html.find(**self.selectors["vacancy_published_at"])

        if published_at is not None:
            published_at = self._parse_published_at(published_at.get_text(strip=True))
        else:
            published_at = datetime.now()

        salary = vacancy_html.find(**self.selectors["vacancy_salary"])

        if salary is not None:
            salary = salary.get_text(strip=True)

        detail = vacancy_html.find(**self.selectors["vacancy_detail"])

        if (detail is not None):
            detail = detail.get_text(strip=True)

        locations = []
        locations_icon = vacancy_html.find("span", **self.selectors["vacancy_locations"]) 

        if locations_icon is not None:
            locations_tag = locations_icon.next_sibling

            if locations_tag is not None:
                locations = locations_tag.get_text(strip=True).split("/")

        company = None
        info = vacancy_html.find(**self.selectors["vacancy_company"])

        if info is not None:
            links = info.find_all("a")

            for info_link in links:
                if "company" in info_link.get("href"):
                    company = info_link.get_text(strip=True)

        vacancy = Vacancy(
            title=title,
            detail=detail,
            link=link,
            company=company,
            locations=locations,
            origin="djinni",
            published_at=published_at,
            salary=salary,
            scrapped_at=datetime.now(),
        )

        return vacancy

    def get_url(self) -> str:
        url: str = f"{self.main_url}keyword-{self.development}/?employment={self.employment}"

        if self.salary is not None:
            url = f"{url}&salary={self.salary}"

        return url

    def scrape(self) -> list[Vacancy]:
        try:
            resource = get_resource(self.get_url())
            soup = BeautifulSoup(resource.content, "html.parser")
            nodes = soup.find_all("li", **self.selectors["vacancy"])
            vacancies = [self.parse_vacancy_html(node) for node in nodes]

            return vacancies
        except Exception as e:
            print(e)
            return []


