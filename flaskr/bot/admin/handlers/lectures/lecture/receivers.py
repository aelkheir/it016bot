import re
from flaskr import db
from flaskr.models import  Document, Lecture, Video, YoutubeLink
from telegram.ext import CallbackContext
from telegram import Update, ReplyKeyboardMarkup
from flaskr.bot.admin.handlers.lectures import list_lecture_files
from flaskr.bot.utils.youtube import get_youtube_video
from flaskr.bot.utils.is_admin import is_admin
from flaskr.bot.admin.admin_constants import  RECIEVIE_LECTURE_FILE, RECIEVE_LECTURE_NUMBER



def recieve_lecture_number(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    # reads from context
    lecture_id = context.chat_data['lecture_id']

    number_regex = re.compile(f'\d+')
    number_match = number_regex.search(update.message.text)

    if number_match:
        lecture = session.query(Lecture).filter(Lecture.id==lecture_id).one()
        lecture.lecture_number = number_match.group()
        session.commit()
        session.close()
        return list_lecture_files(update, context, lecture_id=lecture_id)

    else:
        update.message.reply_text(f'''الرجاء ادخل رقم المحاضرة مباشرة، مثال:
        3''' )
        return RECIEVE_LECTURE_NUMBER

def recieve_lecture_file(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    reply_keyboard = []

    reply_keyboard.append(['رجوع'])

    markup = ReplyKeyboardMarkup(keyboard=reply_keyboard, resize_keyboard=True)

    # reads from context
    lecture_id = context.chat_data['lecture_id']

    lecture = session.query(Lecture).filter(Lecture.id==lecture_id).one()

    file_name = ''
    inserted = False

    if update.message.document:
        file = update.message.document
        file_name = file.file_name if file.file_name else file.file_unique_id + ' [document]'
        doc = Document(file_name=file_name, file_id=file.file_id, file_unique_id=file.file_unique_id)
        doc.lecture = lecture
        session.add(doc)
        inserted = True

    elif update.message.video:
        file = update.message.video
        file_name = file.file_name if file.file_name else file.file_unique_id + ' [video]'
        vid = Video(file_name=file_name, file_id=file.file_id, file_unique_id=file.file_unique_id)
        vid.lecture = lecture
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
            youtube_link.lecture = lecture
            session.add(youtube_link)

            file_name = youtube_video['snippet']['title']
            inserted = True


    
    if inserted:
        session.commit()
        session.close()
        update.message.reply_text(f'تمت اضافة {file_name}', reply_markup=markup)

    
    else :
        update.message.reply_text(f'حدث خطا الرجاء ارسال ملف document', reply_markup=markup)
    
    return RECIEVIE_LECTURE_FILE


