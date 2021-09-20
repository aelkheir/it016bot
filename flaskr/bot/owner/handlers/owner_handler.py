from flaskr.bot.utils.is_owner import is_owner
from flaskr.bot.owner.owner_constants import CHOICE
from flaskr.bot.utils.register_new_user import register_new_user
from flaskr import db
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
import logging
from flaskr.models import User



logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def owner_handler(update: Update, context: CallbackContext) -> int:

    user = update.message.from_user
    logger.info("Owner %s started the conversation.", user.first_name)

    session = db.session

    user = update.message.from_user

    if not is_owner(update, context, session):
        return

    reply_keyboard = []

    reply_keyboard.append(['المستخدمين'])
    reply_keyboard.append(['المدراء'])
    reply_keyboard.append(['تحديث اوامر البوت'])

    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

    update.message.reply_text(
        f'Owner {user.first_name}',
        reply_markup=markup,
    )

    session.close()
    return CHOICE

