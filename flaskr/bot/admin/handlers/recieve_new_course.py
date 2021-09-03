from flaskr.bot.utils.is_admin import is_admin
import re
from flaskr import db
from flaskr.models import  Course
from telegram.ext import CallbackContext, CallbackContext
from flaskr.bot.admin.admin_constants import RECIEVE_NEW_COURSE
from flaskr.bot.admin.handlers.admin_handler import admin_handler
from telegram import Update


new_coures_regex = re.compile(
    f'الاسم: (\w+(\s\w+)*)( - ((\w+)(\s\w+)*))?\n'
    'الرمز:\s(...\d\d\d)',
    re.UNICODE
)

def recieve_new_course(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return


    new_coures_match = new_coures_regex.search(update.message.text)

    if new_coures_match:
        ar_name = new_coures_match.groups()[0]

        en_name = new_coures_match.groups()[3]
        en_name = en_name if en_name else ''

        course_symbol = new_coures_match.groups()[-1]

        course = Course(
            ar_name=ar_name,
            en_name=en_name,
            course_symbol=course_symbol,
        )

        session.add(course)



        session.commit()
        session.close()

        update.message.reply_text(f'تم اضافة {ar_name} {course_symbol}')

        return admin_handler(update, context)

    else:
        update.message.reply_text('الرجاء ادخال الاسم والرمز كما في المثال.')
        return RECIEVE_NEW_COURSE
