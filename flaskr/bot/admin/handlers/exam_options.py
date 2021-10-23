from flaskr.bot.admin.admin_constants import EXAM_FILE_OPTIONS, RECIEVE_EXAM_NAME, RECIEVE_EXAM_FILE
from flaskr.bot.utils.is_admin import is_admin
from flaskr.bot.admin.handlers.course_options import list_exams
from flaskr import db
from flaskr.models import  Course, Exam
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update, ReplyKeyboardRemove
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup



def delete_exam(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    # read from to context
    exam_id = context.chat_data['exam_id']

    exam = session.query(Exam).filter(Exam.id==exam_id).first()

    session.delete(exam)
    update.message.reply_text(f'تم حذف {exam.name}')

    # delete from to context
    del context.chat_data['exam_id']

    session.commit()
    session.close()
    return list_exams(update, context)

def send_exam_old(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    # read from to context
    course_id = context.chat_data['course_id']
    file_name = context.chat_data['file_name']

    file = session.query(Exam).join(Course)\
        .filter(Exam.file_name==file_name)\
        .filter(Course.id==course_id)\
        .first()
        
    if file.file_type == 'document':
        update.message.bot.sendDocument(update.message.chat_id, document=file.file_id)
        
    elif file.file_type == 'photo':
        update.message.bot.sendPhoto(update.message.chat_id, photo=file.file_id)


def edit_exam_name(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    session.close()

    update.message.reply_text(
        'ارسل اسم الامتحان على الصورة، الاسم: اسم الامتحان\n'
        'مثال:\n'
        'الاسم: ميدتيرم 2016-2017'
        , reply_markup=ReplyKeyboardRemove())

    return RECIEVE_EXAM_NAME

def add_file(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    session = db.session

    reply_keyboard = []
    reply_keyboard.append(['رجوع'])
    markup = ReplyKeyboardMarkup(keyboard=reply_keyboard, resize_keyboard=True)

    if not is_admin(update, context, session):
        return

    update.message.reply_text('ارسل ملف document او photo:', reply_markup=markup)

    session.close()
    return RECIEVE_EXAM_FILE

def edit_file(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    file_name = update.message.text

    # write to context
    context.chat_data['file_name'] = file_name

    reply_keyboard = [
        [ 'عرض' ],
        [ 'حذف الملف' ],
        [ 'رجوع' ]
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

    update.message.reply_text(f'{file_name}', reply_markup=markup)
    return EXAM_FILE_OPTIONS
