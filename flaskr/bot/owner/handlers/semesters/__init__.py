from sqlalchemy import func
from flaskr.bot.owner.owner_constants import SEMESTER_OPTIONS
from flaskr.bot.utils.is_owner import is_owner
from flaskr import db
from flaskr.models import Semester
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from flaskr.bot.owner.handlers.manage_semesters import manage_semesters




def edit_semester(update: Update, context: CallbackContext, semester_id=None) -> int:
    session = db.session

    if not is_owner(update, context, session):
        return

    semester = None

    if update.message.text and not semester_id:
      semester_number = int(update.message.text.split(' ')[1])
      semester = session.query(Semester).filter(Semester.number==semester_number).first()
    elif semester_id:
      semester = session.query(Semester).filter(Semester.id==semester_id).first()

    # write to chat data
    context.chat_data['semester_id'] = semester.id

    reply_keyboard = []
    reply_keyboard.append(['اضف للارشيف', f'استخرج من الارشيف'])
    reply_keyboard.append(['حذف السمستر', f'تعديل رقم السمستر: {semester.number}'])
    reply_keyboard.append(['رجوع'])
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(f'سمستر {semester.number}',
            reply_markup=markup,
    )

    session.close()
    return SEMESTER_OPTIONS



def add_semester(update: Update, context: CallbackContext) -> int:
    session = db.session


    if not is_owner(update, context, session):
        return

    last_semester = session.query(func.max(Semester.number)).first()
    semester_number = last_semester[0] + 1 if last_semester[0] else 1

    semester = Semester(number=semester_number)

    session.add(semester)

    session.commit()
    session.close()
    return manage_semesters(update, context)
