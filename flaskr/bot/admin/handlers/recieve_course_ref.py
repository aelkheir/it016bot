from flaskr.bot.admin.admin_constants import RECIEVE_COURSE_REF
from flaskr.bot.utils.is_admin import is_admin
from flaskr import db
from flaskr.models import  Course, Refference
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update, ReplyKeyboardMarkup



def recieve_course_ref(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    reply_keyboard = []

    reply_keyboard.append(['رجوع'])

    markup = ReplyKeyboardMarkup(keyboard=reply_keyboard, resize_keyboard=True)

    # reads from context
    course_id = context.chat_data['course_id']

    course = session.query(Course).filter(Course.id==course_id).one()

    file = update.message.document
    file_name = file.file_name if file.file_name else file.file_unique_id + ' [document]'
    ref = Refference(name=file_name, file_id=file.file_id, file_unique_id=file.file_unique_id)
    ref.course = course
    session.add(ref)

    session.commit()
    session.close()
    update.message.reply_text(f'تم اضافة {file_name}', reply_markup=markup)
    return RECIEVE_COURSE_REF
    