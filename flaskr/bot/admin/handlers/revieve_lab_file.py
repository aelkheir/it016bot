from flaskr.bot.utils.youtube import get_youtube_video
import re
from flaskr.bot.utils.is_admin import is_admin
from flaskr.bot.admin.admin_constants import  RECIEVIE_LAB_FILE
from flaskr import db
from flaskr.models import  Document, Lab, Lecture, Video, YoutubeLink
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update, ReplyKeyboardMarkup


def recieve_lab_file(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    reply_keyboard = []

    reply_keyboard.append(['رجوع'])

    markup = ReplyKeyboardMarkup(keyboard=reply_keyboard, resize_keyboard=True)

    # reads from context
    lab_id = context.chat_data['lab_id']

    lab = session.query(Lab).filter(Lab.id==lab_id).one()

    file_name = ''
    inserted = False

    if update.message.document:
        file = update.message.document
        file_name = file.file_name if file.file_name else file.file_unique_id + ' [document]'
        doc = Document(file_name=file_name, file_id=file.file_id, file_unique_id=file.file_unique_id)
        doc.lab = lab
        session.add(doc)
        inserted = True

    elif update.message.video:
        file = update.message.video
        file_name = file.file_name if file.file_name else file.file_unique_id + ' [video]'
        vid = Video(file_name=file_name, file_id=file.file_id, file_unique_id=file.file_unique_id)
        vid.lab = lab
        session.add(vid)
        inserted = True


    elif update.message.entities and update.message.entities[0].type == 'url':
        url = update.message.text
        id_regex_type1 = re.compile('https://youtu.be/(.+)')
        id_regex_type2 = re.compile('https://www.youtube.com/watch?v=(.+)')
        id_match = id_regex_type1.search(url) if id_regex_type1.search(url) else id_regex_type2.search(url)

        if id_match:
            video_id = id_match.groups()[0]
            youtube_video = get_youtube_video(video_id)
            youtube_link = YoutubeLink(
                video_title=youtube_video['snippet']['title'],
                youtube_id=youtube_video['id'],
                url=url
            )
            youtube_link.lab = lab
            session.add(youtube_link)

            file_name = youtube_video['snippet']['title']
            inserted = True


    
    if inserted:
        session.commit()
        session.close()
        update.message.reply_text(f'تمت اضافة {file_name}', reply_markup=markup)

    
    else :
        update.message.reply_text(f'حدث خطا الرجاء ارسال ملف document', reply_markup=markup)
    
    return RECIEVIE_LAB_FILE

