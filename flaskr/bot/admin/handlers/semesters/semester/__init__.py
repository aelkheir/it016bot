import re
from flaskr.bot.admin.handlers.edit_archive import edit_archive
from flaskr.bot.admin.handlers.semesters import edit_semester
from flaskr.bot.admin.admin_constants import RECIEVE_SEMESTER_NUMBER
from flaskr.bot.utils.get_current_semester import get_current_semester
from flaskr.bot.utils.is_owner import is_owner
from flaskr.models import CurrentSemester, Semester
from flaskr import db
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update, ReplyKeyboardRemove


semester_number_regex = re.compile(r'^\d+$')


def set_to_current_semester(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_owner(update, context, session):
        return

    semester_id = context.chat_data['semester_id']

    semester = session.query(Semester).filter(Semester.id==semester_id).one()

    if semester.current:
        update.message.reply_text('هذا السمستر حالي بالفعل')
        return edit_semester(update, context, semester_id)

    current = get_current_semester(session)

    current.semester = semester

    update.message.reply_text(f'تم وضع السمستر {semester.number} في الحالي')

    session.commit()  
    session.close()

    return edit_semester(update, context, semester_id)



def edit_semester_number(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_owner(update, context, session):
        return

    update.message.reply_text(f'''ادخل رقم السمستر مباشرة، مثال:
    3''', reply_markup=ReplyKeyboardRemove())

    session.close()
    return RECIEVE_SEMESTER_NUMBER


def delete_semester(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_owner(update, context, session):
        return

    semester_id = context.chat_data['semester_id']

    semester = session.query(Semester).filter(Semester.id==semester_id).one()

    session.delete(semester)

    session.commit()  
    session.close()
    return edit_archive(update, context)

