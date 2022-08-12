from flaskr.bot.admin.handlers.assignments import list_assignment_files
from flaskr.bot.admin.handlers.labs import list_lab_files
from flaskr.bot.utils.is_admin import is_admin
from flaskr import db
from flaskr.models import  Assignment, Document, Lab, Photo, Video, YoutubeLink
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update 


def fetch_file(assignment_id, file_name, session):
    assignment = session.query(Assignment).filter(Assignment.id==assignment_id).one()

    for doc in assignment.documents:
        if doc.file_name == file_name:
            return doc

    for photo in assignment.photos:
        if photo.file_name == file_name:
            return photo



def delete_file(update: Update, context: CallbackContext) -> int:
    session = db.session


    if not is_admin(update, context, session):
        return

    # read from to context
    assignment_id = context.chat_data['assignment_id']
    file_name = context.chat_data['file_name']

    file = fetch_file(assignment_id, file_name, session)
    
    if file:
        session.delete(file)
        update.message.reply_text(f'تم حذف {file_name}')

    if not file:
        update.message.reply_text(f'حدث خطا: لا يوجد {file}')
    
    # delete from to context
    del context.chat_data['file_name']

    session.commit()
    session.close()
    return list_assignment_files(update, context, assignment_id==assignment_id)

def send_file(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    # read from to context
    assignment_id = context.chat_data['assignment_id']
    file_name = context.chat_data['file_name']

    file = fetch_file(assignment_id, file_name, session)

    if isinstance(file, Document):
        update.message.bot.sendDocument(update.message.chat_id, document=file.file_id)

    if isinstance(file, Photo):
        update.message.bot.sendPhoto(update.message.chat_id, photo=file.file_id)
    
    return None