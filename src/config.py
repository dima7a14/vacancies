import os

from dotenv import load_dotenv

load_dotenv()

FIREBASE_CREDENTIALS = os.environ.get("FIREBASE_CREDENTIALS", '{"type":"","project_id":"","private_key_id":"","private_key":"","client_email":"","client_id":"","auth_uri":"","token_uri":"","auth_provider_x509_cert_url":"","client_x509_cert_url":""}')
FIREBASE_DB_URL = os.environ.get("FIREBASE_DB_URL", "")
FIREBASE_USER_UID = os.environ.get("FIREBASE_USER_UID", "")
DOU_CATEGORY = os.environ.get("DOU_CATEGORY", "Python")
DOU_LOCATION = os.environ.get("DOU_LOCATION", "remote")
DJINNI_DEVELOPMENT = os.environ.get("DJINNI_DEVELOPMENT", "python")
DJINNI_EMPLOYMENT = os.environ.get("DJINNI_EMPLOYMENT", "remote")
DJINNI_SALARY = int(os.environ.get("DJINNI_SALARY", 5000))
SCRAPE_INTERVAL = int(os.environ.get("SCRAPE_INTERVAL", 1800))
