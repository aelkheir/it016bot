import re
from flaskr.bot.owner.handlers.manage_semesters import manage_semesters
from flaskr.bot.owner.handlers.semesters import edit_semester
from flaskr.bot.owner.owner_constants import RECIEVE_SEMESTER_NUMBER
from flaskr.bot.utils.is_owner import is_owner
from flaskr.models import Semester
from flaskr import db
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update, ReplyKeyboardRemove


semester_number_regex = re.compile(r'^\d+$')


def add_to_archive(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_owner(update, context, session):
        return

    semester_id = context.chat_data['semester_id']

    semester = session.query(Semester).filter(Semester.id==semester_id).one()

    if semester.archived:
        update.message.reply_text(f'السمستر {semester.number} موجود بالفعل في الارشيف')
        session.close()
        return manage_semesters(update, context)

    semester.archived = True


    update.message.reply_text(f'تم اضافة السمستر {semester.number} الى الارشيف')

    session.commit()  
    session.close()

    return edit_semester(update, context, semester_id)

def remove_from_archive(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_owner(update, context, session):
        return

    semester_id = context.chat_data['semester_id']

    semester = session.query(Semester).filter(Semester.id==semester_id).one()

    if not semester.archived:
        update.message.reply_text(f'السمستر {semester.number} ليس موجود في الارشيف')
        session.close()
        return manage_semesters(update, context)

    semester.archived = False

    update.message.reply_text(f'تم استخراج السمستر {semester.number} من الارشيف')

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
    return manage_semesters(update, context)

