from flaskr.bot.utils.is_admin import is_admin
from flaskr import db
from flaskr.bot.admin.admin_constants import  RECIEVE_COURSE_REF, RECIEVE_COURSE_SHEET, REFFERENCE_FILE_OPTIONS, SHEET_FILE_OPTIONS
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup



def add_sheet(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return


    reply_keyboard = []
    reply_keyboard.append(['رجوع'])
    markup = ReplyKeyboardMarkup(keyboard=reply_keyboard, resize_keyboard=True)

    update.message.reply_text('ارسل المرجع، الصيغة المقبولة document (pdf, ...)', reply_markup=markup)
    return RECIEVE_COURSE_SHEET


def edit_sheet(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    file_name = update.message.text

    # write to context
    context.chat_data['file_name'] = file_name

    reply_keyboard = [
        [ 'عرض' ],
        [ 'حذف الشيت' ],
        [ 'رجوع' ]
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

    update.message.reply_text(f'{file_name}', reply_markup=markup)
    return SHEET_FILE_OPTIONS