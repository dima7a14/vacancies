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


def auth(func: Callable):
    allowed_ids: List[int] = [int(id.strip()) for id in os.environ.get("ALLOWED_USERS", "").split(",")]

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

bot = Updater(os.environ.get("TELEGRAM_BOT_TOKEN"), use_context=True)

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


bot.dispatcher.add_handler(CommandHandler("start", show))
bot.dispatcher.add_handler(CommandHandler("show", show))
bot.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
