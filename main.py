from datetime import datetime

import click

from scrappers.common import ScrapperService
from scrappers.vacancy import Vacancy
from scrappers.dou_scrapper import DouScrapper
from db import add_vacancy, clear_vacancies, read_vacancies
from errors import VacancyExistsException

@click.group()
def cli() -> None:
    pass

@click.command()
def search() -> None:
    scrapper = ScrapperService()
    scrapper.register(DouScrapper())
    scrapper.run()

    for vacancy in scrapper.vacancies:
        try:
            add_vacancy({
                "title": vacancy.title,
                "link": vacancy.link,
                "detail": vacancy.detail,
                "company": vacancy.company,
                "origin": vacancy.origin,
                "locations": vacancy.locations,
                "salary": vacancy.salary,
                "published_at": vacancy.published_at,
                "scrapped_at": vacancy.scrapped_at.isoformat(),
            })
            click.echo(f"Added vacancy: {vacancy.title} [{vacancy.link}]")
        except VacancyExistsException as e:
            click.echo(e)

@click.command()
def show() -> None:
    vacancies = [
        Vacancy(
            title=v.get("title"),
            detail=v.get("detail"),
            link=v.get("link"),
            origin=v.get("origin"),
            locations=v.get("locations"),
            company=v.get("company"),
            salary=v.get("salary"),
            published_at=v.get("published_at"),
            scrapped_at=datetime.fromisoformat(v.get("scrapped_at")),
        ) for v in read_vacancies().values()
    ]

    click.echo(vacancies)

@click.command()
def clear() -> None:
    clear_vacancies()
    click.echo("Vacancies cleared")

cli.add_command(search)
cli.add_command(show)
cli.add_command(clear)

if __name__ == "__main__":
    cli()
