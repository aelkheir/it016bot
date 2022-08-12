import re
from sqlalchemy import func
from flaskr.bot.utils.is_admin import is_admin
from flaskr.bot.admin.admin_constants import ASSIGNMENT_OPTIONS, LAB_OPTIONS
from flaskr import db
from flaskr.models import Assignment, Course, Lab
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update 
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from flaskr.bot.admin.handlers.courses.course import list_assignments


def list_assignment_files(update: Update, context: CallbackContext, assignment_id=None) -> int:

    if 'file_name' in context.chat_data:
        del context.chat_data['file_name']

    session = db.session

    if not is_admin(update, context, session):
        return

    if 'assignment_id' in context.chat_data and not assignment_id:
        assignment_id = context.chat_data['assignment_id']

    if not assignment_id:
        assignment_id_regex = re.compile('\(id: (\d+)\)')
        assignment_id_match = assignment_id_regex.search(update.message.text)
        assignment_id = assignment_id_match.groups()[0]

    if assignment_id:
        # write to context
        context.chat_data['assignment_id'] = assignment_id

    # reads from context

    assignment = session.query(Assignment).filter(Assignment.id==int(assignment_id)).one()
        

    reply_keyboard = []

    for document in assignment.documents:
        reply_keyboard.append([f'{document.file_name}'])

    for photo in assignment.photos:
        reply_keyboard.append([f'{photo.file_name}'])
    

    reply_keyboard.append(['اضافة ملف'])
    reply_keyboard.append(['حذف التسليم', f'تعديل رقم التسليم: {assignment.assignment_number}'])
    reply_keyboard.append(['رجوع'])

    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(f'{assignment.course.ar_name}: تسليم رقم {assignment.assignment_number}',
            reply_markup=markup,
    )

    session.close()
    return ASSIGNMENT_OPTIONS


def to_list_lab_files(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    # read from context
    lecture_id = context.chat_data['lecture_id']

    session.close()
    return list_assignment_files(update, context, lecture_id=lecture_id)

def add_assignment(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    # reads from context
    course_id = context.chat_data['course_id']

    course = session.query(Course).filter(Course.id==course_id).one()

    last_assignment = session.query(func.max(Assignment.assignment_number)) \
      .filter_by(course_id=course_id).first()
    assignment_number = last_assignment[0] + 1 if last_assignment[0] else 1

    assignment = Assignment(assignment_number=assignment_number)
    assignment.course = course

    session.add(assignment)

    update.message.reply_text(f'تمت اضافة تسليم جديد بنجاح')

    session.commit()
    session.close()
    return list_assignments(update, context)