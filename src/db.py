import os
import json
from datetime import datetime, timedelta
from typing import Callable

from dotenv import load_dotenv
import firebase_admin
from firebase_admin import db, credentials

from .errors import VacancyExistsException

load_dotenv()

cred = credentials.Certificate(json.loads(os.environ.get("FIREBASE_CREDENTIALS")))
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
    else:
        raise VacancyExistsException(data)


def clear_vacancies() -> None:
    db_ref = db.reference(vacancies_ref)
    db_ref.delete()

def listen_vacancies(cb: Callable) -> None:
    db_ref = db.reference(vacancies_ref)

    db_ref.listen(cb)
