import sched
from apscheduler.schedulers.blocking import BlockingScheduler

from main import scrape

scheduler = BlockingScheduler()

scheduler.add_job(scrape, "interval", seconds=1800)

scheduler.start()
