import os
from typing import Callable, List

from telegram.update import Update
from telegram.ext.updater import Updater
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

from .db import read_vacancies
from .vacancy import Vacancy, parse_vacancy

def get_allowed_ids() -> List[int]:
    return [int(id.strip()) for id in os.environ.get("ALLOWED_USERS", "").split(",")]

def auth(func: Callable):
    allowed_ids = get_allowed_ids()

    def wrapper(update: Update, *args, **kwargs):
        user = update.message.from_user
        
        if user["id"] not in allowed_ids:
            return update.message.reply_text("Access Denied.")
        
        return func(update, *args, **kwargs)
    
    return wrapper

def render_vacancy(vacancy: Vacancy) -> str:
    return f"""
        **[{vacancy.title}]({vacancy.link})**\n
        {vacancy.detail}\n
        **Salary: **{vacancy.salary}
        **Locations: **{", ".join(vacancy.locations)}
        **Company: **{vacancy.company}
        **Origin: **{vacancy.origin}
        **Published at: **{vacancy.published_at}
    """


@auth
def show(update: Update, context: CallbackContext) -> None:
    vacancies = read_vacancies().values()

    if vacancies is None:
        update.message.reply_text("No fresh vacancies.")
    else:
        vacancies = [parse_vacancy(v) for v in read_vacancies().values()]
    
        for vacancy in vacancies:
            update.message.reply_text(render_vacancy(vacancy), parse_mode="markdown")

@auth
def unknown(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f"Sorry, {update.message.text} is not a valid command.")


class Bot:
    def __init__(self) -> None:
        self.updater = Updater(os.environ.get("TELEGRAM_BOT_TOKEN"), use_context=True)
        dp = self.updater.dispatcher

        dp.add_handler(CommandHandler("start", show))
        dp.add_handler(CommandHandler("show", show))
        dp.add_handler(MessageHandler(Filters.command, unknown))

    def start(self) -> None:
        self.updater.start_webhook(listen="0.0.0.0", port=int(os.environ.get("TELEGRAM_BOT_PORT")), url_path=os.environ.get("TELEGRAM_BOT_TOKEN"))
        self.updater.bot.set_webhook(f"https://vacancies-bot.herokuapp.com/{os.environ.get('TELEGRAM_BOT_TOKEN')}")
        
    def send_vacancy(self, vacancy: Vacancy) -> None:
        for chat_id in get_allowed_ids():
            self.updater.bot.send_message(chat_id=chat_id, text=render_vacancy(vacancy), parse_mode="markdown")
