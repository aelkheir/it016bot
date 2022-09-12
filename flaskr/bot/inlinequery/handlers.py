import math
from flaskr.bot.utils.get_user_language import get_user_language
from flaskr.bot.utils.user_required import user_required
from flaskr.models import   Assignment, Course, Document, Exam, Lab, Lecture, Photo, Tutorial, User, Video
from flaskr import db
from telegram.ext import  CallbackContext
from flaskr.bot.localization.ar import ar
from flaskr.bot.localization.en import en
from telegram import   Update, InputMediaVideo, InputMediaPhoto, constants



def inline_help_message(update: Update, context: CallbackContext) -> int:
    session = db.session

    user = user_required(update, context, session)
    user = session.query(User).filter(User.id==user.id).one()

    user.start_count += 1

    language = get_user_language(context.chat_data['language'])

    update.message.reply_text(
        en['inline_help_message'],
        parse_mode=constants.PARSEMODE_MARKDOWN_V2,
        disable_web_page_preview=True
    )

    session.commit()
    session.close()
    return None

def send_lecture(update: Update, context: CallbackContext) -> int:
    session = db.session

    user = user_required(update, context, session)
    user = session.query(User).filter(User.id==user.id).one()

    user.start_count += 1

    language = get_user_language(context.chat_data['language'])

    _, lecture_id = context.args[0].split('-')

    lecture = session.query(Lecture).filter(Lecture.id==lecture_id).one()

    course_name = lecture.course.ar_name \
        if user.language == 'ar' \
        else lecture.course.en_name

    update.message.reply_text(
        f"- {course_name.title()}: {language['lecture'].capitalize()} {lecture.lecture_number}"
    )

    for doc in lecture.documents:
        update.message.bot.sendDocument(update.message.chat_id, document=doc.file_id)
        user.download_count += 1

    media_group = []
    videos = session.query(Video).filter(Video.lecture_id==lecture_id).order_by(Video.id).all()
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
        update.message.bot.sendMediaGroup(update.message.chat.id, media_group)

    for link in lecture.youtube_links:
        update.message.bot.sendMessage(update.message.chat_id, text=link.url)
        user.download_count += 1
        
    session.commit()
    session.close()
    return None


def send_lab(update: Update, context: CallbackContext) -> int:
    session = db.session

    user = user_required(update, context, session)
    user = session.query(User).filter(User.id==user.id).one()

    user.start_count += 1

    language = get_user_language(context.chat_data['language'])

    _, lab_id = context.args[0].split('-')

    lab = session.query(Lab).filter(Lab.id==lab_id).one()

    course_name = lab.course.ar_name \
        if user.language == 'ar' \
        else lab.course.en_name

    update.message.reply_text(
        f"- {course_name.title()}: {language['lab'].capitalize()} {lab.lab_number}"
    )

    for doc in lab.documents:
        update.message.bot.sendDocument(update.message.chat_id, document=doc.file_id)
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
        update.message.bot.sendMediaGroup(update.message.chat.id, media_group)

    for link in lab.youtube_links:
        update.message.bot.sendMessage(update.message.chat_id, text=link.url)
        user.download_count += 1
        
    session.commit()
    session.close()
    return None

def send_tutorial(update: Update, context: CallbackContext) -> int:
    session = db.session

    user = user_required(update, context, session)
    user = session.query(User).filter(User.id==user.id).one()

    user.start_count += 1

    language = get_user_language(context.chat_data['language'])

    _, tutorial_id = context.args[0].split('-')

    tutorial = session.query(Tutorial).filter(Tutorial.id==tutorial_id).one()

    course_name = tutorial.course.ar_name \
        if user.language == 'ar' \
        else tutorial.course.en_name

    update.message.reply_text(
        f"- {course_name.title()}: {language['tutorial'].capitalize()} {tutorial.tutorial_number}"
    )

    for doc in tutorial.documents:
        update.message.bot.sendDocument(update.message.chat_id, document=doc.file_id)
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
        update.message.bot.sendMediaGroup(update.message.chat.id, media_group)


    for link in tutorial.youtube_links:
        update.message.bot.sendMessage(update.message.chat_id, text=link.url)
        user.download_count += 1
        
    session.commit()
    session.close()
    return None


def send_references(update: Update, context: CallbackContext) -> int:
    session = db.session

    user = user_required(update, context, session)
    user = session.query(User).filter(User.id==user.id).one()

    user.start_count += 1

    language = get_user_language(context.chat_data['language'])

    _, course_id = context.args[0].split('-')

    course = session.query(Course).filter(Course.id==course_id).one()

    course_name = course.ar_name \
        if user.language == 'ar' \
        else course.en_name

    update.message.reply_text(
        f"- {course_name.title()}: {language['references'].capitalize()}"
    )

    for reference in course.refferences:
        update.message.bot.sendDocument(update.message.chat_id, document=reference.file_id)
        user.download_count += 1

        
    session.commit()
    session.close()
    return None

def send_assignment(update: Update, context: CallbackContext) -> int:
    session = db.session

    user = user_required(update, context, session)
    user = session.query(User).filter(User.id==user.id).one()

    user.start_count += 1

    language = get_user_language(context.chat_data['language'])

    _, assignment_id = context.args[0].split('-')

    assignment = session.query(Assignment).filter(Assignment.id==assignment_id).one()

    course_name = assignment.course.ar_name \
        if user.language == 'ar' \
        else assignment.course.en_name

    photos = session.query(Photo)\
        .filter(Photo.assignment_id == assignment_id)\
        .order_by(Photo.id).all()

    documents = session.query(Document)\
        .filter(Document.assignment_id == assignment_id)\
        .order_by(Document.id).all()

    media_group = []
    for (i, photo) in enumerate(photos):
        album_caption = f"{language['assignment'].capitalize()} {assignment.assignment_number}"
        input_media = InputMediaPhoto(
            photo.file_id,
            caption=album_caption if i == 0 else None
        )
        media_group.append(input_media)

    update.message.reply_text(
        f"- {course_name.title()}: {language['assignment'].capitalize()} {assignment.assignment_number}"
    )

    if media_group:
        update.message.bot.sendMediaGroup(update.message.chat.id, media_group)

    for doc in documents:
        update.message.bot.sendDocument(update.message.chat.id, document=doc.file_id)

    user.download_count += 1

        
    session.commit()
    session.close()
    return None

def send_exam(update: Update, context: CallbackContext) -> int:
    session = db.session

    user = user_required(update, context, session)
    user = session.query(User).filter(User.id==user.id).one()

    user.start_count += 1

    language = get_user_language(context.chat_data['language'])

    _, exam_id = context.args[0].split('-')

    exam = session.query(Exam).filter(Exam.id==exam_id).one()

    course_name = exam.course.ar_name

    photos = session.query(Photo)\
        .filter(Photo.exam_id == exam_id)\
        .order_by(Photo.id).all()

    documents = session.query(Document)\
        .filter(Document.exam_id == exam_id)\
        .order_by(Document.id).all()

    media_groups = []
    group_index = -1
    for (i, photo) in enumerate(photos):
        if i % 10 == 0:
            group_index += 1
            media_groups.append([])
        album_caption = ''
        if i % 10 == 0 and i < 10:
            album_caption =f"{course_name}\n{exam.name}\n"
        if len(photos) > 10 and i % 10 == 0:
            album_caption = album_caption +  f"{ar['album']} {group_index + 1}/{math.ceil(len(photos)/10)}\n"
        album_caption = album_caption if album_caption else None
        input_media = InputMediaPhoto(
            photo.file_id,
            caption=album_caption
        )
        media_groups[group_index].append(input_media)

    for media_group in media_groups:
        update.message.bot.sendMediaGroup(update.message.chat.id, media_group)

    for doc in documents:
        update.message.bot.sendDocument(update.message.chat.id, document=doc.file_id)

    user.download_count += 1

    session.commit()
    session.close()
    return None
