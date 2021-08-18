from flaskr.bot.utils.is_admin import is_admin
import re
from flaskr.bot.admin.admin_constants import CONFIRM_COURSE_DELETION
from flaskr import db
from flaskr.models import Course
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update, ReplyKeyboardRemove
from flaskr.bot.admin.handlers.admin_handler import admin_handler

def apply_delete_course(update: Update, context: CallbackContext) -> int:

    session = db.session

    if not is_admin(update, context, session):
        return

    confirmation_regex = re.compile('نعم\sانا\sمتاكد\sتماما.')

    confirmation_match = confirmation_regex.search(update.message.text)

    # reads from context
    course_id = context.chat_data['course_id']

    if confirmation_match:
        course = session.query(Course).filter(Course.id == course_id).one()
        course_name = course.name
        session.delete(course)
        session.commit()
        session.close()
        update.message.reply_text(f'تم حذف {course_name}')
        # delete from context
        del context.chat_data['course_id']
        return admin_handler(update, context)

    update.message.reply_text(f'''رجاءا للتاكيد ادخل: 
    نعم انا متاكد تماما.''', reply_markup=ReplyKeyboardRemove())

    session.close()
    return CONFIRM_COURSE_DELETION
