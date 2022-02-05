import re
from telegram import Update, ReplyKeyboardRemove
from flaskr import db
from telegram.ext import CallbackContext
from flaskr.models import Course
from flaskr.bot.admin.admin_constants import RECIEVE_NAME_SYMBOL, CONFIRM_COURSE_DELETION
from flaskr.bot.admin.handlers.admin_handler import admin_handler
from flaskr.bot.utils.is_admin import is_admin
from flaskr.bot.admin.handlers.courses import edit_course


name_regex = re.compile(r'الاسم: (\w+(\s\w+)*)( - ((\w+)(\s\w+)*))?', re.UNICODE)

symbol_regex = re.compile(r'الرمز: (\w{3}\d{3})( - (\w+\d+))?', re.UNICODE)

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
        ar_course_symbol = symbol_match.groups()[0]

        en_course_symbol = symbol_match.groups()[2]
        en_course_symbol = en_course_symbol if en_course_symbol else ''

        course.course_symbol = ar_course_symbol
        course.en_course_symbol = en_course_symbol
    
    if symbol_match or name_match:
        session.commit()
        course_name = course.ar_name
        session.close()
        update.message.reply_text(f'تم التعديل بنجاح')
        return edit_course(update, context, course_name=course_name)
    elif not (symbol_match or name_match):
        update.message.reply_text(f'الرجاء الاتزام بالطريقة الموضحة في المثال')
        return RECIEVE_NAME_SYMBOL


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
        course_name = course.ar_name
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
