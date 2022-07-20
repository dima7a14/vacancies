import click

from src.config import SPECIALIZATIONS, LOCATIONS, SALARIES
from src.vacancy import parse_vacancy
from src.scrappers.common import Location, ScrapperService, Scrapper, Specialization
from src.scrappers.dou_scrapper import make_dou_scrappers
from src.scrappers.djinni_scrapper import make_djinni_scrappers
from src.scrappers.fwdays_scrapper import make_fwdays_scrappers
from src.db import add_vacancy, clear_vacancies, read_vacancies, listen_vacancies
from src.errors import VacancyExistsException
from src.telegram_bot import Bot


def scrape(scrappers: list[Scrapper]) -> None:
    scrapper_service = ScrapperService()
    for scrapper in scrappers:
        scrapper_service.register(scrapper)
    scrapper_service.run()

    for vacancy in scrapper_service.vacancies:
        try:
            add_vacancy({
                "title": vacancy.title,
                "link": vacancy.link,
                "detail": vacancy.detail,
                "company": vacancy.company,
                "origin": vacancy.origin,
                "locations": vacancy.locations,
                "salary": vacancy.salary,
                "published_at": vacancy.published_at.isoformat(),
                "scrapped_at": vacancy.scrapped_at.isoformat(),
            })
            click.echo(f"Added vacancy: {vacancy.title} [{vacancy.link}]")
        except VacancyExistsException as e:
            click.echo(e)

@click.group()
def cli() -> None:
    pass

@click.command()
def search() -> None:
    scrape([
        *make_dou_scrappers(SPECIALIZATIONS, LOCATIONS),
        *make_djinni_scrappers(SPECIALIZATIONS, LOCATIONS, SALARIES),
        *make_fwdays_scrappers(SPECIALIZATIONS, LOCATIONS)
    ])


@click.command()
def run() -> None:
    run_bot()
    scrape([
        *make_dou_scrappers(SPECIALIZATIONS, LOCATIONS),
        *make_djinni_scrappers(SPECIALIZATIONS, LOCATIONS, SALARIES),
        *make_fwdays_scrappers(SPECIALIZATIONS, LOCATIONS)
    ])

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

def run_bot() -> None:
    bot = Bot()

    def notify(event: dict):
        if event.path != "/" and event.data:
            bot.send_vacancy(parse_vacancy(event.data))


    listen_vacancies(notify)
    bot.start()
    click.echo("Telegram bot is running...")

@click.command()
def start_bot() -> None:
    run_bot()

cli.add_command(search)
cli.add_command(show)
cli.add_command(clear)
cli.add_command(start_bot)
cli.add_command(run)

if __name__ == "__main__":
    cli()
