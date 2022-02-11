import re
from flaskr.bot.owner.owner_constants import RECIEVE_SEMESTER_NUMBER
from flaskr.bot.utils.is_owner import is_owner
from flaskr import db
from flaskr.models import Semester
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update
from flaskr.bot.owner.handlers.semesters import edit_semester


semester_number_regex = re.compile(r'^\d+$')

def receive_semester_number(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_owner(update, context, session):
        return

    semester_id = context.chat_data['semester_id']

    number_match = semester_number_regex.match(update.message.text)

    if number_match:
        semester = session.query(Semester).filter(Semester.id==semester_id).one()
        semester.number = int(number_match.group())

        session.commit()
    
    else:
        update.message.reply_text(f'''الرجاء ادخل رقم السمستر كما في المثال''' )
        return RECIEVE_SEMESTER_NUMBER


    session.close()
    return edit_semester(update, context, semester_id)


