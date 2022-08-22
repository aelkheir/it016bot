from flaskr.bot.utils.is_admin import is_admin
from flaskr.bot.admin.admin_constants import LECTURE_FILE_OPTIONS, PUBLISH_LECTURE, RECIEVE_LECTURE_NUMBER, RECIEVIE_LECTURE_FILE
from flaskr import db
from flaskr.models import  Lecture
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup
from flaskr.bot.admin.handlers.courses.course import list_lectures


def delete_lecture(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    # reads from context
    lecture_id = context.chat_data['lecture_id']

    lecture = session.query(Lecture).filter(Lecture.id==lecture_id).one()
    session.delete(lecture)

    update.message.reply_text(f'تم حذف {lecture.course.ar_name} {lecture.lecture_number}')

    session.commit()
    session.close()
    return list_lectures(update, context)


def edit_lecture_number(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    update.message.reply_text(f'''ادخل رقم المحاضرة مباشرة، مثال:
    3''', reply_markup=ReplyKeyboardRemove())

    session.close()
    return RECIEVE_LECTURE_NUMBER


def add_file(update: Update, context: CallbackContext) -> int:
    session = db.session

    reply_keyboard = []
    reply_keyboard.append(['رجوع'])
    markup = ReplyKeyboardMarkup(keyboard=reply_keyboard, resize_keyboard=True)

    if not is_admin(update, context, session):
        return

    update.message.reply_text('ارسل ملف document او video او youtube link:', reply_markup=markup)

    session.close()
    return RECIEVIE_LECTURE_FILE


def edit_file(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    file_name = update.message.text

    # write to context
    context.chat_data['file_name'] = file_name

    reply_keyboard = [
        [ 'عرض' ],
        [ 'حذف الملف' ],
        [ 'رجوع' ]
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

    update.message.reply_text(f'{file_name}', reply_markup=markup)

    session.close()
    return LECTURE_FILE_OPTIONS

def publish(update: Update, context: CallbackContext) -> int:
    session = db.session

    # reads from context
    lecture_id = context.chat_data['lecture_id']

    lecture = session.query(Lecture).filter(Lecture.id==lecture_id).one()

    reply_keyboard = [
        ['ارسل تنبيه', 'نشر بصمت'],
        ['رجوع']
    ]
    markup = ReplyKeyboardMarkup(keyboard=reply_keyboard, resize_keyboard=True)

    if not is_admin(update, context, session):
        return

    status = 'منشور' if lecture.published  else 'غير منشور'
    update.message.reply_text(f'الوضع الحالي: {status}', reply_markup=markup)

    session.close()
    return PUBLISH_LECTURE
