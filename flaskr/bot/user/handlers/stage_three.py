import math
from flaskr.bot.localization import ar
from flaskr.bot.utils.buttons import back_to_assignments_button, back_to_labs_button, back_to_tutorials_button
from flaskr.bot.user.user_constants import ASSIGNMENT, FILE, LAB, SHOW_GLOBAL_NOTE, STAGE_FOURE, TUTORIAL
from flaskr.bot.utils.get_user_language import get_user_language
from flaskr.bot.utils.user_required import user_required
from flaskr.models import  Assignment, Course, Document, Exam, Lab, Lecture, Photo, Refference, Sheet, Tutorial, User,  Video, YoutubeLink
from flaskr import db
from telegram.ext import  CallbackContext
from telegram import  InputMediaVideo, InputMediaPhoto, Update, InlineKeyboardButton, InlineKeyboardMarkup 


def list_lab_files(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)
    language = get_user_language(context.chat_data['language'])

    _, lab_id = query.data.split(' ')

    lab = session.query(Lab).filter(Lab.id==lab_id).one()
    course = lab.course


    keyboard = []

    for document in lab.documents:
        keyboard.append([
            InlineKeyboardButton(
                f'{document.file_name}',
                callback_data=f'{FILE} {document.id} {document.file_unique_id}'
            )
        ])

    for video in lab.videos:
        keyboard.append([
            InlineKeyboardButton(
                f'{video.file_name}',
                callback_data=f'{FILE} {video.id} {video.file_unique_id}'
            )
        ])

    for youtube_link in lab.youtube_links:
        keyboard.append([
            InlineKeyboardButton(f'{youtube_link.video_title}',
            callback_data=f'{FILE} {youtube_link.id}')
        ])

    if len(lab.documents) + len(lab.videos) + len(lab.youtube_links) > 1:
        keyboard.append([InlineKeyboardButton(
            f"{language['download']} {language['all']} {language['files']}".title(),
            callback_data=f'{LAB} {lab.id}')
        ])

    course_name = course.ar_name \
        if user.language == 'ar' \
        else course.en_name
    course_name = course_name if course_name else course.ar_name


    keyboard.append([
        back_to_labs_button(language, user.language, course.id),
    ])

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(
        text=f"{course_name}: {language['lab'].capitalize()} {lab.lab_number}",
        reply_markup=reply_markup
    )

    session.close()
    return STAGE_FOURE

def list_tutorial_files(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)
    language = get_user_language(context.chat_data['language'])

    _, tutorial_id = query.data.split(' ')

    tutorial = session.query(Tutorial).filter(Tutorial.id==tutorial_id).one()
    course = tutorial.course

    keyboard = []

    for document in tutorial.documents:
        keyboard.append([
            InlineKeyboardButton(
                f'{document.file_name}',
                callback_data=f'{FILE} {document.id} {document.file_unique_id}'
            )
        ])

    for video in tutorial.videos:
        keyboard.append([
            InlineKeyboardButton(
                f'{video.file_name}',
                callback_data=f'{FILE} {video.id} {video.file_unique_id}'
            )
        ])

    for youtube_link in tutorial.youtube_links:
        keyboard.append([
            InlineKeyboardButton(f'{youtube_link.video_title}',
            callback_data=f'{FILE} {youtube_link.id}')
        ])

    if len(tutorial.documents) + len(tutorial.videos) + len(tutorial.youtube_links) > 1:
        keyboard.append([InlineKeyboardButton(
            f"{language['download']} {language['all']} {language['files']}".title(),
            callback_data=f'{TUTORIAL} {tutorial.id}')
        ])

    course_name = course.ar_name \
        if user.language == 'ar' \
        else course.en_name
    course_name = course_name if course_name else course.ar_name

    keyboard.append([
        back_to_tutorials_button(language, user.language, course.id),
    ])

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(
        text=f"{course_name}: {language['tutorial'].capitalize()} {tutorial.tutorial_number}",
        reply_markup=reply_markup
    )

    session.close()
    return STAGE_FOURE


def send_file(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)
    user = session.query(User).filter(User.id==user.id).one()

    file_unique_id = None

    try: 
        _, file_id, file_unique_id = query.data.split(' ')
    except ValueError:
        _, file_id  = query.data.split(' ')

    file_unique_id = file_unique_id or None

    doc = None
    vid = None
    link = None

    if file_unique_id:
        doc = session.query(Document) \
            .filter(Document.id==file_id, Document.file_unique_id==file_unique_id) \
            .one_or_none()

        vid = session.query(Video) \
            .filter(Video.id==file_id, Video.file_unique_id==file_unique_id) \
            .one_or_none()

        link = session.query(YoutubeLink).filter(YoutubeLink.id==file_id).one_or_none()
    else:
        doc = session.query(Document) \
            .filter(Document.id==file_id) \
            .one_or_none()

        vid = session.query(Video) \
            .filter(Video.id==file_id) \
            .one_or_none()

        link = session.query(YoutubeLink).filter(YoutubeLink.id==file_id).one_or_none()

    if doc:
        query.bot.sendDocument(query.message.chat.id, document=doc.file_id)
        user.download_count += 1

    elif vid:
        query.bot.sendVideo(query.message.chat.id, video=vid.file_id, caption=vid.file_name)
        user.download_count += 1

    elif link:
        query.bot.sendMessage(query.message.chat.id, text=link.url)
        user.download_count += 1
        
    session.commit()
    session.close()
    return None

def send_all_labs(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)
    language = get_user_language(context.chat_data['language'])

    _, course_id = query.data.split(' ')

    course = session.query(Course).filter(Course.id==course_id).one()

    # read from context
    user_id = context.user_data['user_id']
    user = session.query(User).filter(User.id==user_id).one()

    course_name = course.ar_name \
        if user.language == 'ar' \
        else course.en_name
    course_name = course_name if course_name else course.ar_name

    for lab in course.labs:
        query.message.reply_text(
            f"- {course_name}: {language['lab'].capitalize()} {lab.lab_number}"
        )

        for doc in lab.documents:
            query.bot.sendDocument(query.message.chat.id, document=doc.file_id)
            user.download_count += 1

        for vid in lab.videos:
            query.bot.sendVideo(query.message.chat.id, video=vid.file_id, caption=vid.file_name)
            user.download_count += 1

        for link in lab.youtube_links:
            query.bot.sendMessage(query.message.chat.id, text=link.url)
            user.download_count += 1
        
    session.commit()
    session.close()
    return None

def send_all_lecture_files(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    if query:
        query.answer()

    user = user_required(update, context, session)
    user = session.query(User).filter(User.id==user.id).one()

    language = get_user_language(context.chat_data['language'])

    _, lecture_id = query.data.split(' ')

    lecture = session.query(Lecture).filter(Lecture.id==lecture_id).one()

    course_name = lecture.course.ar_name \
        if user.language == 'ar' \
        else lecture.course.en_name

    query.message.reply_text(
        f"- {course_name}: {language['lecture'].capitalize()} {lecture.lecture_number}"
    )

    for doc in lecture.documents:
        query.bot.sendDocument(query.message.chat.id, document=doc.file_id)
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
        query.bot.sendMediaGroup(query.message.chat.id, media_group)


    for link in lecture.youtube_links:
        query.bot.sendMessage(query.message.chat.id, text=link.url)
        user.download_count += 1
        
    session.commit()
    session.close()
    return None

def send_course_refference(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)
    user = session.query(User).filter(User.id==user.id).one()

    _, refference_id = query.data.split(' ')

    refference = session.query(Refference).filter(Refference.id==refference_id).one()

    query.bot.sendDocument(query.message.chat.id, document=refference.file_id)
    user.download_count += 1

        
    session.commit()
    session.close()
    return None

def send_course_sheet(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)
    user = session.query(User).filter(User.id==user.id).one()

    _, sheet_id = query.data.split(' ')

    sheet = session.query(Sheet).filter(Sheet.id==sheet_id).one()

    query.bot.sendDocument(query.message.chat.id, document=sheet.file_id)
    user.download_count += 1

        
    session.commit()
    session.close()
    return None

def send_all_course_refferences(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)
    user = session.query(User).filter(User.id==user.id).one()

    language = get_user_language(context.chat_data['language'])

    _, course_id = query.data.split(' ')

    course = session.query(Course).filter(Course.id==course_id).one()

    course_name = course.ar_name \
        if user.language == 'ar' \
        else course.en_name
    course_name = course_name if course_name else course.ar_name

    if len(course.refferences) > 0:
        query.message.reply_text(
        f"{course_name}: {language['references'].capitalize()}",
        )
        for refference in course.refferences:
            query.bot.sendDocument(query.message.chat.id, document=refference.file_id)
            user.download_count += 1

    session.commit()
    session.close()
    return None

def send_all_course_sheets(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)
    user = session.query(User).filter(User.id==user.id).one()

    language = get_user_language(context.chat_data['language'])

    _, course_id = query.data.split(' ')

    course = session.query(Course).filter(Course.id==course_id).one()

    course_name = course.ar_name \
        if user.language == 'ar' \
        else course.en_name
    course_name = course_name if course_name else course.ar_name

    if len(course.sheets) > 0:
        query.message.reply_text(
        f"{course_name}: {language['sheets'].capitalize()}",
        )
        for sheet in course.sheets:
            query.bot.sendDocument(query.message.chat.id, document=sheet.file_id)
            user.download_count += 1

    session.commit()
    session.close()
    return None


def send_assignment(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)
    user = session.query(User).filter(User.id==user.id).one()

    language = get_user_language(context.chat_data['language'])

    _, assignment_id = query.data.split(' ')

    assignment = session.query(Assignment).filter(Assignment.id==assignment_id).one()

    course = assignment.course

    course_name = course.ar_name \
        if user.language == 'ar' \
        else course.en_name
    course_name = course_name if course_name else course.ar_name

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

    query.message.reply_text(
        f"- {course_name}: {language['assignment'].capitalize()} {assignment.assignment_number}"
    )

    if media_group:
        query.bot.sendMediaGroup(query.message.chat.id, media_group)

    for doc in documents:
        query.bot.sendDocument(query.message.chat.id, document=doc.file_id)

    user.download_count += 1


    session.commit()
    session.close()
    return None

def send_course_exam(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)
    user = session.query(User).filter(User.id==user.id).one()

    language = get_user_language(context.chat_data['language'])

    _, exam_id = query.data.split(' ')

    exam = session.query(Exam).filter(Exam.id==exam_id).one()

    course = exam.course

    course_name = course.ar_name \
        if user.language == 'ar' \
        else course.en_name
    course_name = course_name if course_name else course.ar_name

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
            album_caption =f"{course.ar_name}\n{exam.name}\n"
        if len(photos) > 10 and i % 10 == 0:
            album_caption = album_caption +  f"{ar['album']} {group_index + 1}/{math.ceil(len(photos)/10)}\n"
        album_caption = album_caption if album_caption else None
        input_media = InputMediaPhoto(
            photo.file_id,
            caption=album_caption
        )
        media_groups[group_index].append(input_media)

    for media_group in media_groups:
        query.bot.sendMediaGroup(query.message.chat.id, media_group)

    for doc in documents:
        query.bot.sendDocument(query.message.chat.id, document=doc.file_id)

    user.download_count += 1

    session.commit()
    session.close()
    return None

def send_all_course_exams(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)
    user = session.query(User).filter(User.id==user.id).one()
    
    language = get_user_language(context.chat_data['language'])

    _, course_id = query.data.split(' ')

    course = session.query(Course).filter(Course.id==course_id).one()

    course_name = course.ar_name \
        if user.language == 'ar' \
        else course.en_name
    course_name = course_name if course_name else course.ar_name

    exams = session.query(Exam).filter(Exam.course_id==course_id)\
        .order_by(Exam.date.desc()).all()

    for exam in exams:

        query.message.reply_text(f"- {course_name}: {exam.name}")

        photos = session.query(Photo)\
            .filter(Photo.exam_id == exam.id)\
            .order_by(Photo.id).all()

        documents = session.query(Document)\
            .filter(Document.exam_id == exam.id)\
            .order_by(Document.id).all()

        for (i, photo) in enumerate(photos):
            page = f"{i + 1} {language['of']} {len(photos)}"

            query.bot.sendPhoto(
                query.message.chat.id,
                photo=photo.file_id,
                caption=f'{page}'
            )

        for doc in documents:
            query.bot.sendDocument(query.message.chat.id, document=doc.file_id)

        user.download_count += 1


    session.commit()
    session.close()
    return None
