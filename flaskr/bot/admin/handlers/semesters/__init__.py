from sqlalchemy import func
from flaskr.bot.admin.admin_constants import SEMESTER_OPTIONS
from flaskr.bot.utils.is_owner import is_owner
from flaskr import db
from flaskr.models import Course, Semester
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from flaskr.bot.admin.handlers.edit_archive import edit_archive
from flaskr.bot.utils.get_current_semester import get_current_semester




def edit_semester(update: Update, context: CallbackContext, semester_id=None) -> int:
    session = db.session

    if not is_owner(update, context, session):
        return

    semester = None

    if 'semester_id' in context.chat_data:
        semester = session.query(Semester).filter(Semester.id==context.chat_data['semester_id']).one()

    else:
      if semester_id:
        semester = session.query(Semester).filter(Semester.id==semester_id).first()

      elif not update.message.text == 'رجوع':
        semester_number = int(update.message.text.split(' ')[1])
        semester = session.query(Semester).filter(Semester.number==semester_number).first()

    # delete from contetxt
    if 'course_id' in context.chat_data:
      del context.chat_data['course_id']

    # write to chat data
    context.chat_data['semester_id'] = semester.id
    context.chat_data['semester_number'] = semester.number


    courses = session.query(Course) \
      .filter(Course.semester_id==semester.id) \
      .order_by(Course.id).all()

    reply_keyboard = []

    for course in courses:
        reply_keyboard.append([
            course.ar_name
        ])

    reply_keyboard.append(['اضافة مادة', f'وضع للحالي'])
    reply_keyboard.append(['حذف السمستر', f'تعديل رقم السمستر: {semester.number}'])
    reply_keyboard.append(['رجوع'])

    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

    status = ' (حالي)' if semester.current else ''
    update.message.reply_text(f'سمستر {semester.number}{status}',
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

    if semester_number == 1:
      current = get_current_semester(session)

      current.semester = semester

    session.commit()
    session.close()
    return edit_archive(update, context)
