from datetime import date
from flaskr.bot.admin.handlers.course_options import list_exams
from flaskr.bot.admin.handlers.exam_options import edit_exam_name
from flaskr.bot.admin.handlers.exams_list import edit_exam
from flaskr.bot.utils.is_admin import is_admin
from flaskr.bot.admin.admin_constants import RECIEVE_EXAM_NAME, RECIEVE_NAME_SYMBOL
import re
from flaskr import db
from flaskr.models import Course, Exam
from telegram.ext import CallbackContext, CallbackContext
from flaskr.bot.admin.handlers.course_overview import course_overview
from telegram import Update, ReplyKeyboardRemove


name_regex = re.compile(r'الاسم: (\w+(\s\w+)*)', re.UNICODE)

date_regex = re.compile(r'\d{4}', re.UNICODE)


def recieve_exam_name(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    name_match = name_regex.search(update.message.text)

    course = None

    if not 'exam_id' in context.chat_data:
        course_id = context.chat_data['course_id']

        course = session.query(Course).filter(Course.id==course_id).one()

    if name_match:
        ar_name = name_match.groups()[0]

        date_match = date_regex.search(ar_name)

        exam = None

        if not 'exam_id' in context.chat_data:
            exam = Exam(name=ar_name)

            if date_match:
                year =  int(date_match.group())
                exam.date = date(year, 1, 1)

            exam.course = course

            update.message.reply_text(f'تم اضافة الامتحان')


        elif 'exam_id' in context.chat_data:
            exam_id = context.chat_data['exam_id']
            exam = session.query(Exam).filter(Exam.id==exam_id).first()
            exam.name = ar_name

            if date_match:
                year =  int(date_match.group())
                exam.date = date(year, 1, 1)

            update.message.reply_text(f'تم تعديل اسم الامتحان')

        session.commit()

        exam_id = exam.id

        session.close()

        return edit_exam(update, context, exam_id=exam_id)



    elif not  name_match:

        update.message.reply_text(f'الرجاء الاتزام بالطريقة الموضحة في المثال')

        return RECIEVE_EXAM_NAME

