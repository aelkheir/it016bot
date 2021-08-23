from flaskr.bot.utils.is_admin import is_admin
from flaskr import db
from flaskr.bot.admin.admin_constants import  EXAM_OPTIONS, RECIEVE_COURSE_EXAM, RECIEVE_COURSE_REF, REFFERENCE_OPTIONS
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update 
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup


def add_exam(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    reply_keyboard = []
    reply_keyboard.append(['رجوع'])
    markup = ReplyKeyboardMarkup(keyboard=reply_keyboard, resize_keyboard=True)

    update.message.reply_text(
        'ارسل الامتحان، الصيغة المقبولة document (pdf, ...) او photo.\n'
        'ضع تعليق على الامتحان في شكل: (نوع الامتحان) (العام الدراسي).\n'
        'مثال: ميدتيرم 2016-2017\n'
        , reply_markup=markup)
    return RECIEVE_COURSE_EXAM


def edit_exam(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    file_name = update.message.text

    # write to context
    context.chat_data['file_name'] = file_name

    reply_keyboard = [
        [ 'عرض' ],
        [ 'حذف الامتحان' ],
        [ 'رجوع' ]
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

    update.message.reply_text(f'{file_name}', reply_markup=markup)
    return EXAM_OPTIONS