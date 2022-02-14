from flaskr.bot.utils.is_admin import is_admin
import re
from flaskr import db
from flaskr.models import  Course
from telegram.ext import CallbackContext, CallbackContext
from flaskr.bot.admin.admin_constants import RECIEVE_NEW_COURSE
from flaskr.bot.admin.handlers.admin_handler import admin_handler
from telegram import Update


new_coures_regex = re.compile(
    r'الاسم: (\w+(\s\w+)*)( - ((\w+)(\s\w+)*))?\n'
    r'الرمز: (\w{3}\d{3})( - (\w+\d+))?',
    re.UNICODE
)

def recieve_new_course(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    # read from context
    semester_id = context.chat_data['semester_id'] if 'semester_id' in context.chat_data else None

    new_coures_match = new_coures_regex.search(update.message.text)

    if new_coures_match:
        ar_name = new_coures_match.groups()[0]

        en_name = new_coures_match.groups()[3]
        en_name = en_name if en_name else ''

        ar_course_symbol = new_coures_match.groups()[6]

        en_course_symbol = new_coures_match.groups()[8]
        en_course_symbol = en_course_symbol if en_course_symbol else ''

        course = Course(
            ar_name=ar_name,
            en_name=en_name,
            course_symbol=ar_course_symbol,
            en_course_symbol=en_course_symbol,
            semester_id=semester_id,
        )

        session.add(course)

        session.commit()
        session.close()

        update.message.reply_text(f'تم اضافة {ar_name} {ar_course_symbol}')

        handler = context.chat_data['back_from_edit_course']

        return handler(update, context)

    else:
        update.message.reply_text('الرجاء ادخال الاسم والرمز كما في المثال.')
        return RECIEVE_NEW_COURSE

