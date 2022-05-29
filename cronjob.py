from apscheduler.schedulers.blocking import BlockingScheduler

from env import DOU_CATEGORY, DOU_LOCATION, DJINNI_DEVELOPMENT, DJINNI_EMPLOYMENT, DJINNI_SALARY, SCRAPE_INTERVAL
from src.scrappers.dou_scrapper import DouScrapper
from src.scrappers.djinni_scrapper import DjinniScrapper
from main import DJINNI_EMPLOYMENT, scrape

def scrape_job() -> None:
    scrape(scrapper_getters=[
        lambda: DouScrapper(category=DOU_CATEGORY, location=DOU_LOCATION),
        lambda: DjinniScrapper(development=DJINNI_DEVELOPMENT, employment=DJINNI_EMPLOYMENT, salary=DJINNI_SALARY)
    ])

scheduler = BlockingScheduler()

scheduler.add_job(scrape_job, "interval", seconds=SCRAPE_INTERVAL)

scheduler.start()
