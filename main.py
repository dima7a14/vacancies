from datetime import datetime

from scrappers.common import ScrapperService
from scrappers.dou_scrapper import DouScrapper
from db import add_vacancy, clear_vacancies, read_vacancies

def main():
    scrapper = ScrapperService()
    scrapper.register(DouScrapper())
    scrapper.run()

    # clear_vacancies()


    vacancies = read_vacancies()

    print("vacancies length", len(vacancies))

    for vacancy in vacancies.values():
        print(vacancy.get("scrapped_at"))

    # for vacancy in scrapper.vacancies:
    #     add_vacancy({
    #         "title": vacancy.title,
    #         "link": vacancy.link,
    #         "detail": vacancy.detail,
    #         "company": vacancy.company,
    #         "origin": vacancy.origin,
    #         "locations": vacancy.locations,
    #         "salary": vacancy.salary,
    #         "published_at": vacancy.published_at,
    #         "scrapped_at": datetime.now().isoformat(),
    #     })


if __name__ == "__main__":
    main()