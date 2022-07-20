from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum

from bs4 import BeautifulSoup, Tag
import dateparser

from .common import Specialization, Location, get_resource
from ..vacancy import Vacancy


class FwdaysLocation(Enum):
    ONLINE = 2
    UKRAINE = 13


class FwdaysSpecialization(Enum):
    PYTHON = 2
    JAVASCRIPT = 3
    FRONTEND = 8
    NODEJS = 9
    REACT = 10


@dataclass
class FwdaysScrapper:
    main_url: str = field(init=False, default="https://fwdays.com/jobs/")
    selectors: dict[str, dict[str, str]] = field(init=False, default_factory=lambda: {
        "vacancy": {"class_": "vacancy"},
        "vacancy_link": {"selector": ".vacancy__title"},
        "vacancy_title": {"selector": ".vacancy__title"},
        "vacancy_published_at": {"selector": ".vacancy__top .vacancy__hint"},
        "vacancy_info": {"selector": ".vacancy__info"},
        "vacancy_detail": {"selector": ".vacancy__desc"},
    })
    specializations: list[FwdaysSpecialization] = field(default_factory=lambda: list())
    locations: list[FwdaysLocation] = field(default_factory=lambda: list())

    def parse_vacancy_html(self, vacancy_html: Tag) -> Vacancy:
        link = vacancy_html.select(self.selectors["vacancy_link"]["selector"])

        if len(link) > 0:
            link = f"{self.main_url}{link[0].get('href')[1:]}"

        title = vacancy_html.select(self.selectors["vacancy_title"]["selector"])

        if len(title) > 0:
            title = title[0].get_text(strip=True)

        published_at = vacancy_html.select(self.selectors["vacancy_published_at"]["selector"])

        if len(published_at) > 0:
            published_at = dateparser.parse(published_at[0].get_text(strip=True))
        else:
            published_at = datetime.now()

        detail = vacancy_html.select(self.selectors["vacancy_detail"]["selector"])

        if len(detail) > 0:
            detail = detail[0].get_text(strip=True)
            
        info = vacancy_html.select(self.selectors["vacancy_info"]["selector"])

        if len(info) > 0:
            info = info[0].get_text(strip=True)
            detail += f"\n\n{info}"

        company = ""
        salary = None
        locations = []

        vacancy = Vacancy(
            title=title,
            detail=detail,
            link=link,
            company=company,
            locations=locations,
            origin="Fwdays",
            published_at=published_at,
            salary=salary,
            scrapped_at=datetime.now(),
        )

        return vacancy

    @property
    def resource_url(self) -> str:
        specializations = "&".join([f"specialization[]={s.value}" for s in self.specializations])
        locations = "&".join([f"city[]={l.value}" for l in self.locations])
        query = specializations

        if locations:
            if query:
                query += f"&{locations}"
            else:
                query = locations

        return f"{self.main_url}?{query}"
        

    def scrape(self) -> list[Vacancy]:
        try:
            resource = get_resource(self.resource_url)
            soup = BeautifulSoup(resource.content, "html.parser")
            nodes = soup.find_all("div", **self.selectors["vacancy"])
            vacancies = [self.parse_vacancy_html(node) for node in nodes]

            return vacancies
        except Exception as e:
            print(e)
            return []



def make_fwdays_scrappers(specializations: list[Specialization], locations: list[Location]) -> list[FwdaysScrapper]:
    fwdays_specializations: list[FwdaysSpecialization] = []
    fwdays_locations: list[FwdaysLocation] = []

    for specialization in specializations:
        match specialization:
            case Specialization.FRONTEND.value:
                fwdays_specializations.extend([FwdaysSpecialization.FRONTEND, FwdaysSpecialization.JAVASCRIPT, FwdaysSpecialization.REACT])
            case Specialization.PYTHON.value:
                fwdays_specializations.append(FwdaysSpecialization.PYTHON)
            case Specialization.NODEJS.value:
                fwdays_specializations.append(FwdaysSpecialization.NODEJS)
            case _:
                print(f"There is no match for specialization {specialization} in FwdaysScrapper")

    for location in locations:
        match location:
            case Location.REMOTE.value:
                fwdays_locations.append(FwdaysLocation.ONLINE)
            case Location.UKRAINE.value:
                fwdays_locations.append(FwdaysLocation.UKRAINE)
            case _:
                print(f"There is no match for location {location} in FwdaysScrapper")

    return [FwdaysScrapper(specializations=fwdays_specializations, locations=fwdays_locations)]

