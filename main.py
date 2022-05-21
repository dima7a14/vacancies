from datetime import datetime

import click

from src.scrappers.common import ScrapperService
from src.vacancy import Vacancy, parse_vacancy
from src.scrappers.dou_scrapper import DouScrapper
from src.db import add_vacancy, clear_vacancies, read_vacancies
from src.errors import VacancyExistsException
from src.telegram_bot import bot

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
        parse_vacancy(v) for v in read_vacancies().values()
    ]

    click.echo(vacancies)

@click.command()
def clear() -> None:
    clear_vacancies()
    click.echo("Vacancies cleared")

@click.command()
def start_bot() -> None:
    bot.start_polling()
    click.echo("Telegram bot is running...")

cli.add_command(search)
cli.add_command(show)
cli.add_command(clear)
cli.add_command(start_bot)

if __name__ == "__main__":
    cli()
