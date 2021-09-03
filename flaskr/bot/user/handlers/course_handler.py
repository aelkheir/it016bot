from telegram.ext import  CallbackContext
from telegram import  Update
from flaskr.bot.utils.user_required import user_required
from flaskr.models import  Course
from flaskr.bot.user.handlers.course_overview import course_overview
from flaskr import db


def course_handler(update: Update, context: CallbackContext) -> int:
    session = db.session

    user_required(update, context, session)

    en_course_symbol = update.message.text[1:]

    course = session.query(Course).filter(Course.en_course_symbol==en_course_symbol).one()
    course_id = course.id

    session.close()

    return course_overview(update, context, course_id)