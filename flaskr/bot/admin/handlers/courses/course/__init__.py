from flaskr.bot.utils.is_admin import is_admin
import re
from flaskr.bot.admin.admin_constants import ASSIGNMENTS_LIST, CONFIRM_COURSE_DELETION, EXAMS_LIST, LABS_LIST, RECIEVE_COURSE_SEMESTER, RECIEVE_NAME_SYMBOL, LECTURES_LIST, REFFERENCES_LIST
import math
from flaskr import db
from flaskr.models import Assignment, Course, Exam, Lab, Lecture, Semester
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
    update.message.reply_text(f'{course.ar_name}: المحاضرات',
            reply_markup=markup,
    )

    session.close()
    return LECTURES_LIST

def list_labs(update: Update, context: CallbackContext) -> int:

    if 'lab_id' in context.chat_data:
        del context.chat_data['lab_id']

    session = db.session

    if not is_admin(update, context, session):
        return

    # reads from context
    course_id = context.chat_data['course_id']

    course = session.query(Course).filter(Course.id==course_id).one()

    labs = session.query(Lab)\
        .filter(Lab.course_id==course_id)\
        .order_by(Lab.lab_number).all()
    
    reply_keyboard = []

    for row_index in range(0, math.ceil(len(labs) / 3)):
        row = []
        is_row_full =  len(labs) // 3 >= row_index + 1
        row_size = 3 if is_row_full else len(labs) % 3
        row_start = row_index * 3

        for lab_index in range(row_start, row_start + row_size):
            lab = labs[lab_index]
            row.append( f'لاب رقم: {lab.lab_number}\n(id: {lab.id})')

        reply_keyboard.append(row)

    reply_keyboard.append(['رجوع', 'اضافة لاب'])

    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(f'{course.ar_name}: اللابات',
            reply_markup=markup,
    )

    session.close()
    return LABS_LIST

def list_assignments(update: Update, context: CallbackContext) -> int:

    if 'assignment_id' in context.chat_data:
        del context.chat_data['assignment_id']

    session = db.session

    if not is_admin(update, context, session):
        return

    # reads from context
    course_id = context.chat_data['course_id']

    course = session.query(Course).filter(Course.id==course_id).one()

    assignments = session.query(Assignment)\
        .filter(Assignment.course_id==course_id)\
        .order_by(Assignment.assignment_number).all()
    
    reply_keyboard = []

    for row_index in range(0, math.ceil(len(assignments) / 3)):
        row = []
        is_row_full =  len(assignments) // 3 >= row_index + 1
        row_size = 3 if is_row_full else len(assignments) % 3
        row_start = row_index * 3

        for assignment_index in range(row_start, row_start + row_size):
            assignment = assignments[assignment_index]
            row.append( f'تسليم رقم: {assignment.assignment_number}\n(id: {assignment.id})')

        reply_keyboard.append(row)

    reply_keyboard.append(['رجوع', 'اضافة تسليم'])

    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(f'{course.ar_name}: التساليم',
            reply_markup=markup,
    )

    session.close()
    return ASSIGNMENTS_LIST




def list_refferences(update: Update, context: CallbackContext) -> int:
    session = db.session

    # delet from context
    if 'file_name' in context.chat_data:
        del context.chat_data['file_name']

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

    if 'exam_id' in context.chat_data:
        del context.chat_data['exam_id']

    # reads from context
    course_id = context.chat_data['course_id']

    course = session.query(Course).filter(Course.id==course_id).one()

    exams = session.query(Exam).filter(Exam.course_id==course_id)\
        .order_by(Exam.date.desc()).all()

    reply_keyboard = []
    

    for exam in exams:
        reply_keyboard.append([f'{exam.name}'])

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
        example = f'''الرمز: رمز المادة [- الرمز بالانجليزية]
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

def edit_course_semester(update: Update, context: CallbackContext) -> int:

    session = db.session

    if not is_admin(update, context, session):
        return

    semesters =  session.query(Semester).order_by(Semester.number).all()

    reply_keyboard = []

    for row_index in range(0, math.ceil(len(semesters) / 2)):
        row = []
        is_row_full =  len(semesters) // 2 >= row_index + 1
        row_size = 2 if is_row_full else len(semesters) % 2
        row_start = row_index * 2

        for semester_index in range(row_start, row_start + row_size):
            semester = semesters[semester_index]
            status = ' (حالي)' if semester.current else ''
            row.append( f'سمستر {semester.number}{status}')

        reply_keyboard.append(row)

    reply_keyboard.append(['رجوع'])

    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)


    update.message.reply_text(f'اختر سمستر', reply_markup=markup)
    return RECIEVE_COURSE_SEMESTER