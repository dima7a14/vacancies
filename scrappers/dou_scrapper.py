from bs4 import BeautifulSoup, ResultSet, Tag
from dataclasses import dataclass, field

from scrappers.common import ScrapperSelectors, get_resource
from .vacancy import Vacancy


@dataclass
class DouScrapper:
    main_url: str = field(init=False, default="https://jobs.dou.ua/vacancies/")
    selectors: ScrapperSelectors = field(init=False, default_factory=lambda: ScrapperSelectors(
        vacancy_selector="vacancy",
        vacancy_link_selector="vt",
        vacancy_title_selector="vt",
        vacancy_date_selector="date",
        vacancy_salary_selector="salary",
        vacancy_locations_selector="cities",
        vacancy_detail_selector="sh-info",
        vacancy_company_selector="company",
        vacancy_more_selector="more-btn",
    ))
    category: str = field(default="Front End")
    location: str = field(default="remote")

    def parse_vacancy_html(self, vacancy_html: Tag) -> Vacancy:
        link = vacancy_html.find(class_=self.selectors.vacancy_link_selector).get("href")

        title = vacancy_html.find(class_=self.selectors.vacancy_title_selector)

        if title is not None:
            title = title.get_text(strip=True)

        date = vacancy_html.find(class_=self.selectors.vacancy_date_selector)

        if date is not None:
            date = date.get_text(strip=True)

        salary = vacancy_html.find(class_=self.selectors.vacancy_salary_selector)

        if salary is not None:
            salary = salary.get_text(strip=True)

        locations = vacancy_html.find(class_=self.selectors.vacancy_locations_selector)

        if locations is not None:
            locations = locations.get_text(strip=True).split(", ")
        else:
            locations = []

        detail = vacancy_html.find(class_=self.selectors.vacancy_detail_selector)

        if detail is not None:
            detail = detail.get_text(strip=True)

        company = vacancy_html.find(class_=self.selectors.vacancy_company_selector)

        if company is not None:
            company = company.get_text(strip=True)

        vacancy = Vacancy(
            title=title,
            detail=detail,
            link=link,
            company=company,
            locations=locations,
            origin="DOU",
            published_at=date,
            salary=salary,
        )

        return vacancy

    def scrape(self) -> list[Vacancy]:
        resource = get_resource(self.main_url)
        soup = BeautifulSoup(resource.content, "html.parser")
        blocks = soup.find_all("div", class_=self.selectors.vacancy_selector)
        vacancies = [self.parse_vacancy_html(block) for block in blocks]

        return vacancies


