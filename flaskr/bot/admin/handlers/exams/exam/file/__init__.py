from flaskr.bot.admin.handlers.exams import edit_exam
from flaskr.bot.utils.is_admin import is_admin
from flaskr import db
from flaskr.models import  Document, Exam, Photo
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update 


def fetch_file(exam_id, file_name, session):
    exam = session.query(Exam).filter(Exam.id==exam_id).one()

    for doc in exam.documents:
        if doc.file_name == file_name:
            return doc

    for photo in exam.photos:
        if photo.file_name == file_name:
            return photo




def delete_file(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    # read from to context
    exam_id = context.chat_data['exam_id']
    file_name = context.chat_data['file_name']

    file = fetch_file(exam_id, file_name, session)
    
    session.delete(file)
    update.message.reply_text(f'تم حذف {file_name}')

    # delete from to context
    del context.chat_data['file_name']

    session.commit()
    session.close()
    return edit_exam(update, context)

def send_file(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    # read from to context
    exam_id = context.chat_data['exam_id']
    file_name = context.chat_data['file_name']

    file = fetch_file(exam_id, file_name, session)

    if isinstance(file, Document):
        update.message.bot.sendDocument(update.message.chat_id, document=file.file_id)

    if isinstance(file, Photo):
        update.message.bot.sendPhoto(update.message.chat_id, photo=file.file_id)

    return None