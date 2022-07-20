from apscheduler.schedulers.blocking import BlockingScheduler

from src.config import SPECIALIZATIONS, LOCATIONS, SALARIES, SCRAPE_INTERVAL
from src.scrappers.dou_scrapper import make_dou_scrappers
from src.scrappers.djinni_scrapper import make_djinni_scrappers
from src.scrappers.fwdays_scrapper import make_fwdays_scrappers
from main import scrape

def scrape_job() -> None:
    scrape([
        *make_dou_scrappers(SPECIALIZATIONS, LOCATIONS),
        *make_djinni_scrappers(SPECIALIZATIONS, LOCATIONS, SALARIES),
        *make_fwdays_scrappers(SPECIALIZATIONS, LOCATIONS)
    ])

scheduler = BlockingScheduler()

scheduler.add_job(scrape_job, "interval", seconds=SCRAPE_INTERVAL)

scheduler.start()
