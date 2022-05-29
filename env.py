import os

from dotenv import load_dotenv

load_dotenv()

DOU_CATEGORY = os.environ.get("DOU_CATEGORY", "Python")
DOU_LOCATION = os.environ.get("DOU_LOCATION", "remote")
DJINNI_DEVELOPMENT = os.environ.get("DJINNI_DEVELOPMENT", "python")
DJINNI_EMPLOYMENT = os.environ.get("DJINNI_EMPLOYMENT", "remote")
DJINNI_SALARY = int(os.environ.get("DJINNI_SALARY", 5000))
SCRAPE_INTERVAL = int(os.environ.get("SCRAPE_INTERVAL", 1800))
