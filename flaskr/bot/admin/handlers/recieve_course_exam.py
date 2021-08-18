from flaskr.bot.admin.handlers.course_options import list_exams
import re
from telegram.files.photosize import PhotoSize
from telegram.files.document import Document
from flaskr.bot.admin.admin_constants import RECIEVE_COURSE_EXAM
from flaskr.bot.utils.is_admin import is_admin
from flaskr import db
from flaskr.models import  Course, Exam
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update, ReplyKeyboardMarkup

exam_name_regex = re.compile('(.*)\s(\d{4}-\d{4})')


def recieve_course_exam(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    reply_keyboard = []

    reply_keyboard.append(['رجوع'])

    markup = ReplyKeyboardMarkup(keyboard=reply_keyboard, resize_keyboard=True)

    text = ''
    file = None

    if update.message.reply_to_message:
        reply_to_message = update.message.reply_to_message
        text = update.message.text

        if reply_to_message.document:
            file = reply_to_message.document

        elif reply_to_message.photo:
            file = reply_to_message.photo[-1]
    
    else:
        message = update.message

        if message.caption:
            text = message.caption

        if message.document:
            file = message.document

        elif message.photo:
            file = message.photo[-1]

    if not text or not file:
        update.message.reply_text('الرجاء ارسال الامتحان وعليه caption.')
        return RECIEVE_COURSE_EXAM
    
    exam_name_match = exam_name_regex.search(text)
    if not exam_name_match:
        update.message.reply_text('الرجاء كتابة ال caption كما في المثال.')
        return RECIEVE_COURSE_EXAM
    
    exam_name = ' '.join(exam_name_match.groups())

    # reads from context
    course_id = context.chat_data['course_id']

    course = session.query(Course).filter(Course.id==course_id).one()

    if isinstance(file, Document):
        file_type = 'document'
        exam = Exam(
            file_name=exam_name,
            file_id=file.file_id,
            file_unique_id=file.file_unique_id,
            file_type=file_type
        )
        exam.course = course
        session.add(exam)
        update.message.reply_text(f'تم اضافة {exam_name}', reply_markup=markup)

    elif isinstance(file, PhotoSize):
        file_type = 'photo'
        exam = Exam(
            file_name=exam_name,
            file_id=file.file_id,
            file_unique_id=file.file_unique_id,
            file_type=file_type
        )
        exam.course = course
        session.add(exam)
        update.message.reply_text(f'تم اضافة {exam_name}', reply_markup=markup)


    session.commit()
    session.close()
    return list_exams(update, context)
    