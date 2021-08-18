from flaskr.bot.utils.user_required import user_required
import telegram
from flaskr.bot.utils.register_new_user import register_new_user
import logging
from flaskr.models import Course, User
from flaskr import db
from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from flaskr.bot.user.user_constants import   COURSE, COURSE_OVERVIEW


logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update: Update, context: CallbackContext) -> int:
    """Send message on `/start`."""
    session = db.session

    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)

    user = user_required(update, context, session)

    user.start_count += 1

    courses =  session.query(Course).all()

    keyboard = []

    for course in courses:
        keyboard.append([
            InlineKeyboardButton(f'{course.name} ({len(course.lectures)})',
            callback_data=f'{COURSE} {course.id}'),
        ])

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("اختر مادة:", reply_markup=reply_markup)

    session.commit()
    session.close()
    return COURSE_OVERVIEW
