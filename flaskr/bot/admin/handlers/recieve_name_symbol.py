from flaskr.bot.utils.is_admin import is_admin
from flaskr.bot.admin.admin_constants import RECIEVE_NAME_SYMBOL
import re
from flaskr import db
from flaskr.models import Course
from telegram.ext import CallbackContext, CallbackContext
from flaskr.bot.admin.handlers.course_overview import course_overview
from telegram import Update, ReplyKeyboardRemove


name_regex = re.compile('الاسم: (\w+(\s\w+)*)( - ((\w+)(\s\w+)*))?', re.UNICODE)

symbol_regex = re.compile('الرمز:\s(.+)', re.UNICODE)

def recieve_name_symbol(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    course_id = context.chat_data['course_id']

    name_match = name_regex.search(update.message.text)

    symbol_match = symbol_regex.search(update.message.text)
    
    course = session.query(Course).filter(Course.id==course_id).one()

    if name_match:
        ar_name = name_match.groups()[0]

        en_name = name_match.groups()[3]
        en_name = en_name if en_name else ''

        course.ar_name = ar_name
        course.en_name = en_name

    elif symbol_match:
        course_symbol = symbol_match.groups()[0]
        course.course_symbol = course_symbol
    
    if symbol_match or name_match:
        session.commit()
        course_name = course.ar_name
        session.close()
        update.message.reply_text(f'تم التعديل بنجاح')
        return course_overview(update, context, course_name=course_name)
    elif not (symbol_match or name_match):
        update.message.reply_text(f'الرجاء الاتزام بالطريقة الموضحة في المثال')
        return RECIEVE_NAME_SYMBOL

