from flaskr.bot.utils.is_admin import is_admin
import re
from flaskr import db
from flaskr.models import  Course
from telegram.ext import CallbackContext, CallbackContext
from flaskr.bot.admin.admin_constants import RECIEVE_NEW_COURSE
from flaskr.bot.admin.handlers.admin_handler import admin_handler
from telegram import Update, ReplyKeyboardRemove


new_coures_regex = re.compile(f'الاسم:\s(.*)\nالرمز:\s(...\d\d\d)')

def recieve_new_course(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    new_coures_match = new_coures_regex.search(update.message.text)

    if new_coures_match:
        course_name = new_coures_match.groups()[0]
        course_symbol = new_coures_match.groups()[1]
        course = Course(name=course_name, course_symbol=course_symbol)
        session.add(course)

        update.message.reply_text(f'تم اضافة {course.name} {course.course_symbol}')

        session.commit()
        session.close()
        return admin_handler(update, context)

    else:
        update.message.reply_text('الرجاء ادخال الاسم والرمز كما في المثال.')
        return RECIEVE_NEW_COURSE
