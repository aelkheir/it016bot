from flaskr.bot.utils.is_admin import is_admin
from flaskr.bot.admin.admin_constants import RECIEVE_LECTURE_NUMBER
import re
from flaskr import db
from flaskr.models import  Lecture
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update, ReplyKeyboardRemove
from flaskr.bot.admin.handlers.lectures_list import list_files



def recieve_lecture_number(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    # reads from context
    lecture_id = context.chat_data['lecture_id']

    number_regex = re.compile(f'\d+')
    number_match = number_regex.search(update.message.text)

    if number_match:
        lecture = session.query(Lecture).filter(Lecture.id==lecture_id).one()
        lecture.lecture_number = number_match.group()
        session.commit()
        session.close()
        return list_files(update, context, lecture_id=lecture_id)

    else:
        update.message.reply_text(f'''الرجاء ادخل رقم المحاضرة مباشرة، مثال:
        3''' )
        return RECIEVE_LECTURE_NUMBER
