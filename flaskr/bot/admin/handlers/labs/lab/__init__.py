from flaskr.bot.utils.is_admin import is_admin
from flaskr.bot.admin.admin_constants import LAB_FILE_OPTIONS, RECIEVE_LAB_NUMBER, RECIEVIE_LAB_FILE
from flaskr import db
from flaskr.models import  Lab
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup
from flaskr.bot.admin.handlers.courses.course import list_labs


def delete_lab(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    # reads from context
    lab_id = context.chat_data['lab_id']

    lab = session.query(Lab).filter(Lab.id==lab_id).one()
    session.delete(lab)

    update.message.reply_text(f'تم حذف {lab.course.ar_name} لاب رقم {lab.lab_number}')

    session.commit()
    session.close()
    return list_labs(update, context)


def edit_lab_number(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    update.message.reply_text(f'''ادخل رقم اللاب مباشرة، مثال:
    3''', reply_markup=ReplyKeyboardRemove())

    session.close()
    return RECIEVE_LAB_NUMBER


def add_file(update: Update, context: CallbackContext) -> int:
    session = db.session

    reply_keyboard = []
    reply_keyboard.append(['رجوع'])
    markup = ReplyKeyboardMarkup(keyboard=reply_keyboard, resize_keyboard=True)

    if not is_admin(update, context, session):
        return

    update.message.reply_text('ارسل ملف document او video او youtube link:', reply_markup=markup)

    session.close()
    return RECIEVIE_LAB_FILE


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
    return LAB_FILE_OPTIONS