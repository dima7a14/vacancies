from typing import Callable
import click

from src.config import DOU_CATEGORY, DOU_LOCATION, DJINNI_DEVELOPMENT, DJINNI_EMPLOYMENT, DJINNI_SALARY
from src.vacancy import parse_vacancy
from src.scrappers.common import ScrapperService, Scrapper
from src.scrappers.dou_scrapper import DouScrapper
from src.scrappers.djinni_scrapper import DjinniScrapper
from src.db import add_vacancy, clear_vacancies, read_vacancies, listen_vacancies
from src.errors import VacancyExistsException
from src.telegram_bot import Bot


def scrape(scrapper_getters: list[Callable[..., Scrapper]]) -> None:
    scrapper = ScrapperService()
    for scr_getter in scrapper_getters:
        scrapper.register(scr_getter())
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
@click.option("--dou-category", default=DOU_CATEGORY, help="Category of the vacancy on DOU")
@click.option("--dou-location", default=DOU_LOCATION, help="Location of the vacancy on DOU")
@click.option("--djinni-development", default=DJINNI_DEVELOPMENT, help="Development of the vacancy on djinni")
@click.option("--djinni-employment", default=DJINNI_EMPLOYMENT, help="Employment of the vacancy on djinni")
@click.option("--djinni-salary", default=DJINNI_SALARY, help="Salary of the vacancy on djinni")
def search(
    dou_category: str,
    dou_location: str,
    djinni_development: str,
    djinni_employment: str,
    djinni_salary: int,
) -> None:
    scrape(scrapper_getters=[
        lambda: DouScrapper(category=dou_category, location=dou_location),
        lambda: DjinniScrapper(development=djinni_development, employment=djinni_employment, salary=int(djinni_salary)),
    ])

@click.command()
def run() -> None:
    run_bot()
    scrape(scrapper_getters=[
        lambda: DouScrapper(category=DOU_CATEGORY, location=DOU_LOCATION),
        lambda: DjinniScrapper(development=DJINNI_DEVELOPMENT, employment=DJINNI_EMPLOYMENT, salary=DJINNI_SALARY),
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
