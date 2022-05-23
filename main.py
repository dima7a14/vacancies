import click

from src.scrappers.common import ScrapperService
from src.vacancy import parse_vacancy
from src.scrappers.dou_scrapper import DouScrapper
from src.db import add_vacancy, clear_vacancies, read_vacancies, listen_vacancies
from src.errors import VacancyExistsException
from src.telegram_bot import bot, send_vacancy

def scrape(category: str="Front End", location: str="remote") -> None:
    scrapper = ScrapperService()
    scrapper.register(DouScrapper(category=category, location=location))
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

@click.group()
def cli() -> None:
    pass

@click.command()
@click.option("--category", default="Front End", help="Category of the vacancy")
@click.option("--location", default="remote", help="Location of the vacancy")
def search(category: str, location: str) -> None:
    scrape(category, location)

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
    def notify(event: dict):
        if event.path != "/" and event.data:
            send_vacancy(parse_vacancy(event.data))


    listen_vacancies(notify)
    bot.start_polling()
    click.echo("Telegram bot is running...")

cli.add_command(search)
cli.add_command(show)
cli.add_command(clear)
cli.add_command(start_bot)

if __name__ == "__main__":
    cli()
