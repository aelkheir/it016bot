from flaskr.bot.utils.is_admin import is_admin
import re
from flaskr.bot.admin.admin_constants import CONFIRM_COURSE_DELETION, EXAMS_LIST, RECIEVE_NAME_SYMBOL, LECTURES_LIST, REFFERENCES_LIST
import math
from flaskr import db
from flaskr.models import Course, Lecture
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update, ReplyKeyboardRemove
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup


def list_lectures(update: Update, context: CallbackContext) -> int:

    if 'lecture_id' in context.chat_data:
        del context.chat_data['lecture_id']

    session = db.session

    if not is_admin(update, context, session):
        return

    # reads from context
    course_id = context.chat_data['course_id']

    course = session.query(Course).filter(Course.id==course_id).one()

    lectures = session.query(Lecture)\
        .filter(Lecture.course_id==course_id)\
        .order_by(Lecture.lecture_number).all()
    
    reply_keyboard = []

    for row_index in range(0, math.ceil(len(lectures) / 3)):
        row = []
        is_row_full =  len(lectures) // 3 >= row_index + 1
        row_size = 3 if is_row_full else len(lectures) % 3
        row_start = row_index * 3

        for lecture_index in range(row_start, row_start + row_size):
            lecture = lectures[lecture_index]
            row.append( f'المحاضرة رقم: {lecture.lecture_number}\n(id: {lecture.id})')

        reply_keyboard.append(row)

    reply_keyboard.append(['رجوع', 'اضافة محاضرة'])
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(f'{course.ar_name}',
            reply_markup=markup,
    )

    session.close()
    return LECTURES_LIST


def list_refferences(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    # reads from context
    course_id = context.chat_data['course_id']

    course = session.query(Course).filter(Course.id==course_id).one()
    reply_keyboard = []
    
    refferences = course.refferences

    for refference in refferences:
        reply_keyboard.append([f'{refference.name}'])

    reply_keyboard.append(['رجوع', 'اضافة مرجع'])
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(f'مراجع {course.ar_name}',
            reply_markup=markup,
    )

    session.close()
    return REFFERENCES_LIST


def list_exams(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    # reads from context
    course_id = context.chat_data['course_id']

    course = session.query(Course).filter(Course.id==course_id).one()
    reply_keyboard = []
    
    exams = course.exams

    for exam in exams:
        reply_keyboard.append([f'{exam.file_name}'])

    reply_keyboard.append(['رجوع', 'اضافة امتحان'])
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(f'امتحانات {course.ar_name}',
            reply_markup=markup,
    )

    session.close()
    return EXAMS_LIST


def edit_name_symbol(update: Update, context: CallbackContext) -> int:

    session = db.session

    if not is_admin(update, context, session):
        return

    option_regex = re.compile(f'تعديل\sال(.*)')
    option_match = option_regex.search(update.message.text)
    option = option_match.groups()[0]
    example = ''
    if option == 'اسم':
        example = f'''الاسم: اسم المادة [- الاسم بالنجليزية]
        مثال:
        الاسم: فيزياء نووية - Nucliar Physics
        '''
    elif option == 'رمز':
        example = f'''الرمز: رمز المادة
    مثال:
    الرمز: فيز102'''

    update.message.reply_text(f'''ادخل {option} المادة على الصورة
    {example}''', reply_markup=ReplyKeyboardRemove())
    return RECIEVE_NAME_SYMBOL

def confirm_delete_course(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    update.message.reply_text(f'''للتاكيد ادخل: 
    نعم انا متاكد تماما.''', reply_markup=ReplyKeyboardRemove())
    session.close()
    return CONFIRM_COURSE_DELETION
