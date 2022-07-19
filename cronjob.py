from apscheduler.schedulers.blocking import BlockingScheduler

from src.config import DOU_CATEGORY, DOU_LOCATION, DJINNI_DEVELOPMENT, DJINNI_EMPLOYMENT, DJINNI_SALARY, SCRAPE_INTERVAL
from src.scrappers.dou_scrapper import DouScrapper
from src.scrappers.djinni_scrapper import DjinniScrapper
from src.scrappers.fwdays_scrapper import FwdaysScrapper, Specialization, Location
from main import DJINNI_EMPLOYMENT, scrape

def scrape_job() -> None:
    scrape(scrapper_getters=[
        lambda: DouScrapper(category=DOU_CATEGORY, location=DOU_LOCATION),
        lambda: DjinniScrapper(development=DJINNI_DEVELOPMENT, employment=DJINNI_EMPLOYMENT, salary=DJINNI_SALARY),
        lambda: FwdaysScrapper(
            specializations=[
                Specialization.FRONTEND,
                Specialization.JAVASCRIPT,
                Specialization.PYTHON,
                Specialization.REACT,
            ],
            locations=[
                Location.ONLINE,
                Location.UKRAINE,
            ],
        ),
    ])

scheduler = BlockingScheduler()

scheduler.add_job(scrape_job, "interval", seconds=SCRAPE_INTERVAL)

scheduler.start()
