from flaskr.bot.utils.is_admin import is_admin
from flaskr import db
from flaskr.models import Course
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update, ReplyKeyboardMarkup
import logging
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup 
from flaskr.bot.admin.admin_constants import COURSE_OVERVIEW

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def admin_handler(update: Update, context: CallbackContext) -> int:

    user = update.message.from_user
    logger.info("Admin %s started the conversation.", user.first_name)

    session = db.session

    if not is_admin(update, context, session):
        return

    if 'course_id' in context.chat_data:
        del context.chat_data['course_id']
    
    courses = session.query(Course)

    reply_keyboard = []

    for course in courses:
        reply_keyboard.append([
            course.name
        ])
    reply_keyboard.append(['اضافة مادة'])

    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

    update.message.reply_text(
        f'Admin {user.first_name}',
        reply_markup=markup,
    )

    session.close()
    return COURSE_OVERVIEW
