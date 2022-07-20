import os

from dotenv import load_dotenv

load_dotenv()

FIREBASE_CREDENTIALS = os.environ.get("FIREBASE_CREDENTIALS", '{"type":"","project_id":"","private_key_id":"","private_key":"","client_email":"","client_id":"","auth_uri":"","token_uri":"","auth_provider_x509_cert_url":"","client_x509_cert_url":""}')
FIREBASE_DB_URL = os.environ.get("FIREBASE_DB_URL", "")
FIREBASE_USER_UID = os.environ.get("FIREBASE_USER_UID", "")
SPECIALIZATIONS = os.environ.get("SPECIALIZATIONS", "").split(",")
LOCATIONS = os.environ.get("LOCATIONS", "").split(",")
SALARIES = [int(s) for s in os.environ.get("SALARIES", "").split(",") if s != ""]
SCRAPE_INTERVAL = int(os.environ.get("SCRAPE_INTERVAL", 1800))
SENTRY_DSN = os.environ.get("SENTRY_DSN")
