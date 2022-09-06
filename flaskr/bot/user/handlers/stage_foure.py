from flaskr.bot.utils.get_user_language import get_user_language
from flaskr.bot.utils.user_required import user_required
from flaskr.models import Lab, Tutorial, User, Video
from flaskr import db
from telegram.ext import  CallbackContext
from telegram import  Update, InputMediaVideo 




def send_all_lab_files(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)
    user = session.query(User).filter(User.id==user.id).one()

    language = get_user_language(context.chat_data['language'])

    _, lab_id = query.data.split(' ')

    lab = session.query(Lab).filter(Lab.id==lab_id).one()

    course_name = lab.course.ar_name \
        if user.language == 'ar' \
        else lab.course.en_name

    query.message.reply_text(
        f"- {course_name}: {language['lab'].capitalize()} {lab.lab_number}"
    )

    for doc in lab.documents:
        query.bot.sendDocument(query.message.chat.id, document=doc.file_id)
        user.download_count += 1

    media_group = []
    videos = session.query(Video).filter(Video.lab_id==lab_id).order_by(Video.id).all()
    album_caption = 'Left to right, top to bottom\n' if len(videos) > 1 else ''
    for (i, video) in enumerate(videos):
        video_filename = video.file_name
        album_caption = album_caption + f'{video_filename}\n'
    for (i, video) in enumerate(videos):
        user.download_count += 1
        input_media = InputMediaVideo(
            video.file_id,
            caption=album_caption if i == 0 else None,
        )
        media_group.append(input_media)
    if media_group:
        query.bot.sendMediaGroup(query.message.chat.id, media_group)

    for link in lab.youtube_links:
        query.bot.sendMessage(query.message.chat.id, text=link.url)
        user.download_count += 1
        
    session.commit()
    session.close()
    return None

def send_all_tutorial_files(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)
    user = session.query(User).filter(User.id==user.id).one()

    language = get_user_language(context.chat_data['language'])

    _, tutorial_id = query.data.split(' ')

    tutorial = session.query(Tutorial).filter(Tutorial.id==tutorial_id).one()

    course_name = tutorial.course.ar_name \
        if user.language == 'ar' \
        else tutorial.course.en_name

    query.message.reply_text(
        f"- {course_name}: {language['tutorial'].capitalize()} {tutorial.tutorial_number}"
    )

    for doc in tutorial.documents:
        query.bot.sendDocument(query.message.chat.id, document=doc.file_id)
        user.download_count += 1

    media_group = []
    videos = session.query(Video).filter(Video.tutorial_id==tutorial_id).order_by(Video.id).all()
    album_caption = 'Left to right, top to bottom\n' if len(videos) > 1 else ''
    for (i, video) in enumerate(videos):
        video_filename = video.file_name
        album_caption = album_caption + f'{video_filename}\n'
    for (i, video) in enumerate(videos):
        user.download_count += 1
        input_media = InputMediaVideo(
            video.file_id,
            caption=album_caption if i == 0 else None,
        )
        media_group.append(input_media)
    if media_group:
        query.bot.sendMediaGroup(query.message.chat.id, media_group)

    for link in tutorial.youtube_links:
        query.bot.sendMessage(query.message.chat.id, text=link.url)
        user.download_count += 1
        
    session.commit()
    session.close()
    return None
