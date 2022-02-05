from flaskr.bot.utils.is_admin import is_admin
from flaskr.bot.admin.handlers.lectures import list_lecture_files
from flaskr import db
from flaskr.models import  Document, Lecture, Video, YoutubeLink
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update 


def fetch_file(lecture_id, file_name, session):
    lecture = session.query(Lecture).filter(Lecture.id==lecture_id).one()
    file = None

    for doc in lecture.documents:
        if doc.file_name == file_name:
            file = doc
            break

    for vid in lecture.videos:
        if vid.file_name == file_name:
            file = vid
            break

    for link in lecture.youtube_links:
        if link.video_title == file_name:
            file = link
            break
    return file



def delete_file(update: Update, context: CallbackContext) -> int:
    session = db.session


    if not is_admin(update, context, session):
        return

    # read from to context
    lecture_id = context.chat_data['lecture_id']
    file_name = context.chat_data['file_name']

    file = fetch_file(lecture_id, file_name, session)
    
    if file:
        session.delete(file)
        update.message.reply_text(f'تم حذف {file_name}')

    if not file:
        update.message.reply_text(f'حدث خطا: لا يوجد {file}')
    

    # delete from to context
    del context.chat_data['file_name']

    session.commit()
    session.close()
    return list_lecture_files(update, context, lecture_id=lecture_id)

def send_file(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    # read from to context
    lecture_id = context.chat_data['lecture_id']
    file_name = context.chat_data['file_name']

    file = fetch_file(lecture_id, file_name, session)

    if isinstance(file, Document):
        update.message.bot.sendDocument(update.message.chat_id, document=file.file_id)

    if isinstance(file, Video):
        update.message.bot.sendVideo(update.message.chat_id, video=file.file_id)

    if isinstance(file, YoutubeLink):
        update.message.bot.sendMessage(update.message.chat_id, text=file.url)
    
    return None