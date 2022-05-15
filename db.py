import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
import firebase_admin
from firebase_admin import db, credentials

load_dotenv()

cred = credentials.Certificate(os.environ.get("FIREBASE_CRED_PATH"))
firebase_admin.initialize_app(cred, {
    "databaseURL": os.environ.get("FIREBASE_DB_URL")
})

vacancies_ref = "/vacancies"

def read_vacancies() -> map:
    start_date = datetime.now() - timedelta(days=2)
    db_ref = db.reference(vacancies_ref)

    return db_ref.order_by_child("scrapped_at").start_at(start_date.isoformat()).limit_to_first(50).get()

def add_vacancy(data: map) -> None:
    db_ref = db.reference(vacancies_ref)

    existed = db_ref.order_by_child("link").equal_to(data.get("link")).get()

    if len(existed) == 0:
        db_ref.push().set(data)
        print(f"Added vacancy: {data.get('title')} [{data.get('link')}]")
    else:
        print(f"Vacancy {data.get('title')} [{data.get('link')}] is already existed")


def clear_vacancies() -> None:
    db_ref = db.reference(vacancies_ref)
    db_ref.delete()
