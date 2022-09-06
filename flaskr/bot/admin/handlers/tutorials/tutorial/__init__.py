from flaskr.bot.utils.is_admin import is_admin
from flaskr.bot.admin.admin_constants import  PUBLISH_TUTTORIAL, RECIEVE_TUTORIAL_NUMBER,  RECIEVIE_TUTORIAL_FILE, TUTORIAL_FILE_OPTIONS
from flaskr import db
from flaskr.models import  Tutorial
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup
from flaskr.bot.admin.handlers.courses.course import list_tutorials


def delete_tutorial(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    # reads from context
    tutorial_id = context.chat_data['tutorial_id']

    tutotial = session.query(Tutorial).filter(Tutorial.id==tutorial_id).one()
    session.delete(tutotial)

    update.message.reply_text(f'تم حذف {tutotial.course.ar_name} تمرين رقم {tutotial.tutorial_number}')

    session.commit()
    session.close()
    return list_tutorials(update, context)


def edit_tutorial_number(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    update.message.reply_text(f'''ادخل رقم التمرين مباشرة، مثال:
    3''', reply_markup=ReplyKeyboardRemove())

    session.close()
    return RECIEVE_TUTORIAL_NUMBER


def add_file(update: Update, context: CallbackContext) -> int:
    session = db.session

    reply_keyboard = []
    reply_keyboard.append(['رجوع'])
    markup = ReplyKeyboardMarkup(keyboard=reply_keyboard, resize_keyboard=True)

    if not is_admin(update, context, session):
        return

    update.message.reply_text('ارسل ملف document او video او youtube link:', reply_markup=markup)

    session.close()
    return RECIEVIE_TUTORIAL_FILE


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
    return TUTORIAL_FILE_OPTIONS

def publish(update: Update, context: CallbackContext) -> int:
    session = db.session

    # reads from context
    tutorial_id = context.chat_data['tutorial_id']

    tutorial = session.query(Tutorial).filter(Tutorial.id==tutorial_id).one()

    reply_keyboard = [
        ['ارسل تنبيه', 'نشر بصمت'],
        ['رجوع']
    ]
    markup = ReplyKeyboardMarkup(keyboard=reply_keyboard, resize_keyboard=True)

    if not is_admin(update, context, session):
        return

    status = 'منشور' if tutorial.published  else 'غير منشور'
    update.message.reply_text(f'الوضع الحالي: {status}', reply_markup=markup)

    session.close()
    return PUBLISH_TUTTORIAL
