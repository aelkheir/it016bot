from flaskr.bot.utils.is_admin import is_admin
from flaskr.bot.admin.handlers.course_options import list_exams, list_refferences
from flaskr import db
from flaskr.models import  Course, Exam, Refference
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update



def delete_exam(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    # read from to context
    course_id = context.chat_data['course_id']
    file_name = context.chat_data['file_name']

    exams = session.query(Exam).filter(Exam.course_id==course_id).all()

    examination = None
    for exam in exams:
        if exam.file_name == file_name:
            examination = exam
            break
    
    if examination:
        session.delete(examination)
        update.message.reply_text(f'تم حذف {file_name}')

    if not examination:
        update.message.reply_text(f'حدث خطا: لا يوجد {file_name}')
    

    # delete from to context
    del context.chat_data['file_name']

    session.commit()
    session.close()
    return list_exams(update, context)

def send_exam(update: Update, context: CallbackContext) -> int:
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
