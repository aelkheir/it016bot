from flaskr.bot.utils.buttons import back_to_labs_button
from flaskr.bot.user.user_constants import FILE, LAB, STAGE_FOURE
from flaskr.bot.utils.user_required import user_required
from flaskr.models import  Course, Document, Exam, Lab, Lecture, Refference, User,  Video, YoutubeLink
from flaskr import db
from telegram.ext import  CallbackContext
from telegram import  Update, InlineKeyboardButton, InlineKeyboardMarkup


def list_lab_files(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)
    language = context.chat_data['language']

    _, lab_id = query.data.split(' ')

    lab = session.query(Lab).filter(Lab.id==lab_id).one()
    course = lab.course


    keyboard = []

    for document in lab.documents:
        keyboard.append([
            InlineKeyboardButton(f'{document.file_name}', callback_data=f'{FILE} {document.id}')
        ])

    for video in lab.videos:
        keyboard.append([
            InlineKeyboardButton(f'{video.file_name}', callback_data=f'{FILE} {video.id}')
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
        text=f"{course_name}: {language['lab']} {lab.lab_number}".title(),
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

    _, file_id = query.data.split(' ')

    doc = session.query(Document).filter(Document.id==file_id).one_or_none()
    vid = session.query(Video).filter(Video.id==file_id).one_or_none()
    link = session.query(YoutubeLink).filter(YoutubeLink.id==file_id).one_or_none()

    if doc:
        query.bot.sendDocument(query.message.chat.id, document=doc.file_id)
        user.download_count += 1

    elif vid:
        query.bot.sendVideo(query.message.chat.id, video=vid.file_id)
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
    language = context.chat_data['language']

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
            f"- {course_name.title()}: {language['lab'].capitalize()} {lab.lab_number}"
        )

        for doc in lab.documents:
            query.bot.sendDocument(query.message.chat.id, document=doc.file_id)
            user.download_count += 1

        for vid in lab.videos:
            query.bot.sendVideo(query.message.chat.id, video=vid.file_id)
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
    query.answer()

    user = user_required(update, context, session)
    user = session.query(User).filter(User.id==user.id).one()

    language = context.chat_data['language']

    _, lecture_id = query.data.split(' ')

    lecture = session.query(Lecture).filter(Lecture.id==lecture_id).one()

    course_name = lecture.course.ar_name \
        if user.language == 'ar' \
        else lecture.course.en_name

    query.message.reply_text(
        f"- {course_name.title()}: {language['lecture'].capitalize()} {lecture.lecture_number}"
    )

    for doc in lecture.documents:
        query.bot.sendDocument(query.message.chat.id, document=doc.file_id)
        user.download_count += 1

    for vid in lecture.videos:
        query.bot.sendVideo(query.message.chat.id, video=vid.file_id)
        user.download_count += 1

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

def send_all_course_refferences(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)
    user = session.query(User).filter(User.id==user.id).one()

    language = context.chat_data['language']

    _, course_id = query.data.split(' ')

    course = session.query(Course).filter(Course.id==course_id).one()

    course_name = course.ar_name \
        if user.language == 'ar' \
        else course.en_name
    course_name = course_name if course_name else course.ar_name

    if len(course.refferences) > 0:
        query.message.reply_text(
        f"{course_name.title()}: {language['references'].capitalize()}",
        )
        for refference in course.refferences:
            query.bot.sendDocument(query.message.chat.id, document=refference.file_id)
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

    _, exam_id = query.data.split(' ')

    exam = session.query(Exam).filter(Exam.id==exam_id).one()

    if exam.file_type == 'document':
        query.bot.sendDocument(query.message.chat.id, document=exam.file_id)
        user.download_count += 1

    elif exam.file_type == 'photo':
        query.bot.sendPhoto(query.message.chat.id, photo=exam.file_id)
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
    
    language = context.chat_data['language']

    _, course_id = query.data.split(' ')

    course = session.query(Course).filter(Course.id==course_id).one()

    course_name = course.ar_name \
        if user.language == 'ar' \
        else course.en_name
    course_name = course_name if course_name else course.ar_name

    if len(course.exams) > 0:

        query.message.reply_text(
            f"{course_name.title()}: {language['exams'].capitalize()}",
        )

        for exam in course.exams:
            if exam.file_type == 'document':
                query.message.reply_text(f'{exam.file_name}')
                query.bot.sendDocument(query.message.chat.id, document=exam.file_id)
                user.download_count += 1

            elif exam.file_type == 'photo':
                query.message.reply_text(f'{exam.file_name}')
                query.bot.sendPhoto(query.message.chat.id, photo=exam.file_id)
                user.download_count += 1

    session.commit()
    session.close()
    return None
