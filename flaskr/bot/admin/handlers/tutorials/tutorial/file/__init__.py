from flaskr.bot.admin.handlers.labs import list_lab_files
from flaskr.bot.admin.handlers.tutorials import list_tutorial_files
from flaskr.bot.utils.is_admin import is_admin
from flaskr import db
from flaskr.models import  Document, Lab, Tutorial, Video, YoutubeLink
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update 


def fetch_file(tutorial_id, file_name, session):
    lab = session.query(Tutorial).filter(Tutorial.id==tutorial_id).one()

    for doc in lab.documents:
        if doc.file_name == file_name:
            return doc

    for vid in lab.videos:
        if vid.file_name == file_name:
            return vid

    for link in lab.youtube_links:
        if link.video_title == file_name:
            return link

def delete_file(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    # read from to context
    tutorial_id = context.chat_data['tutorial_id']
    file_name = context.chat_data['file_name']

    file = fetch_file(tutorial_id, file_name, session)
    
    if file:
        session.delete(file)
        update.message.reply_text(f'تم حذف {file_name}')

    if not file:
        update.message.reply_text(f'حدث خطا: لا يوجد {file}')
    
    # delete from to context
    del context.chat_data['file_name']

    session.commit()
    session.close()
    return list_tutorial_files(update, context, tutorial_id=tutorial_id)

def send_file(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    # read from to context
    tutorial_id = context.chat_data['tutorial_id']
    file_name = context.chat_data['file_name']

    file = fetch_file(tutorial_id, file_name, session)

    if isinstance(file, Document):
        update.message.bot.sendDocument(
            update.message.chat_id,
            document=file.file_id,
        )

    if isinstance(file, Video):
        update.message.bot.sendVideo(
            update.message.chat_id,
            video=file.file_id,
            caption=file.file_name
        )

    if isinstance(file, YoutubeLink):
        update.message.bot.sendMessage(update.message.chat_id, text=file.url)
    
    return None