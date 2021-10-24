from flaskr.bot.utils.is_admin import is_admin
from flaskr import db
from flaskr.bot.admin.admin_constants import  EXAM_OPTIONS, RECIEVE_EXAM_NAME
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update, ReplyKeyboardRemove
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup

from flaskr.models import Exam


def add_exam(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return


    update.message.reply_text(
        'ارسل اسم الامتحان على الصورة، الاسم: اسم الامتحان\n'
        'مثال:\n'
        'الاسم: ميدتيرم 2016-2017',
        reply_markup=ReplyKeyboardRemove())

    return RECIEVE_EXAM_NAME


def edit_exam(update: Update, context: CallbackContext, exam_id=None) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    exam = None

    if not exam_id and not 'exam_id' in context.chat_data:
        exam = session.query(Exam).filter(Exam.name==update.message.text).first()

        # write to context
        context.chat_data['exam_id'] = exam.id

    elif exam_id:
        exam = session.query(Exam).filter(Exam.id==exam_id).one()

        # write to context
        context.chat_data['exam_id'] = exam.id
    
    elif 'exam_id' in context.chat_data:
        exam_id = context.chat_data['exam_id']
        exam = session.query(Exam).filter(Exam.id==exam_id).one()


    reply_keyboard = []

    for photo in exam.photos:
        reply_keyboard.append([
            photo.file_name
        ])

    for document in exam.documents:
        reply_keyboard.append([
            document.file_name
        ])

    reply_keyboard.append(['اضافة ملف'])
    reply_keyboard.append(['حذف الامتحان', f'تعديل الاسم'])
    reply_keyboard.append(['رجوع'])

    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

    update.message.reply_text(f'{exam.course.ar_name}: {exam.name}', reply_markup=markup)
    return EXAM_OPTIONS