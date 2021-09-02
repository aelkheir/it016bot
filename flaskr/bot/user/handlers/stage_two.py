from flaskr.bot.utils.user_required import user_required
from flaskr.models import Course, Lecture, User
from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from flaskr.bot.user.user_constants import COURSE, EXAM, EXAMS, FILE, LECTURE, REFFERENCES, REFFERENCE, STAGE_THREE, SUBJECT_LIST
from flaskr import db

back_icon ='»'

def list_lecture_files(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user_required(update, context, session)
    language = context.chat_data['language']

    course_id, lecture_id = query.data.split(' ')

    lecture = session.query(Lecture).filter(Lecture.id==lecture_id).one()
    course = lecture.course


    keyboard = []

    for document in lecture.documents:
        keyboard.append([
            InlineKeyboardButton(f'{document.file_name}', callback_data=f'{FILE} {document.id}')
        ])

    for video in lecture.videos:
        keyboard.append([
            InlineKeyboardButton(f'{video.file_name}', callback_data=f'{FILE} {video.id}')
        ])

    for youtube_link in lecture.youtube_links:
        keyboard.append([
            InlineKeyboardButton(f'{youtube_link.video_title}',
            callback_data=f'{FILE} {youtube_link.id}')
        ])

    if len(lecture.documents) + len(lecture.videos) + len(lecture.youtube_links) > 1:
        keyboard.append([InlineKeyboardButton(
            f"{language['download']} {language['all']} {language['files']}".capitalize(),
            callback_data=f'{LECTURE} {lecture.id}')
        ])

    keyboard.append([
        InlineKeyboardButton(f'{course.name} {back_icon}', callback_data=f'{COURSE} {course.id}'),
        InlineKeyboardButton(
        f"{language['back_to_courses']}".capitalize(),
         callback_data=SUBJECT_LIST)
    ])

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=f"{course.name} - {language['lecture']} {lecture.lecture_number}".capitalize(), reply_markup=reply_markup
    )

    session.close()
    return STAGE_THREE


def send_all_lectures(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user_required(update, context, session)
    language = context.chat_data['language']

    _, course_id = query.data.split(' ')

    course = session.query(Course).filter(Course.id==course_id).one()

    # read from context
    user_id = context.user_data['user_id']
    user = session.query(User).filter(User.id==user_id).one()

    for lecture in course.lectures:
        query.message.reply_text(
            f"---- {course.name} - {language['lecture']} {lecture.lecture_number} ----".capitalize()
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


def list_lecture_refferences(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user_required(update, context, session)
    language = context.chat_data['language']

    course_id, _ = query.data.split(' ')

    course = session.query(Course).filter(Course.id==course_id).one()

    keyboard = []

    for refference in course.refferences:
        keyboard.append([
            InlineKeyboardButton(f'{refference.name}', callback_data=f'{REFFERENCE} {refference.id}')
        ])

    if len(course.refferences) > 1:
        keyboard.append([InlineKeyboardButton(
            f"{language['download']} {language['all']} {language['references']}".capitalize(),
            callback_data=f'{REFFERENCES} {course.id}'),
        ])

    keyboard.append([
        InlineKeyboardButton(f'{course.name} {back_icon}', callback_data=f'{COURSE} {course.id}'),
        InlineKeyboardButton(
            f"{language['back_to_courses']}".capitalize(),
            callback_data=SUBJECT_LIST),
    ])

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=f"{language['genitive'](course.name, language['indifinite_references'])}".capitalize(),
        reply_markup=reply_markup
    )
    return STAGE_THREE

def list_lecture_exams(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user_required(update, context, session)
    language = context.chat_data['language']

    course_id, _ = query.data.split(' ')

    course = session.query(Course).filter(Course.id==course_id).one()

    keyboard = []

    for exam in course.exams:
        keyboard.append([
            InlineKeyboardButton(f'{exam.file_name}', callback_data=f'{EXAM} {exam.id}')
        ])

    if len(course.exams) > 1:
        keyboard.append([InlineKeyboardButton(
            f"{language['download']} {language['all']} {language['exams']}".capitalize(),
            callback_data=f'{EXAMS} {course.id}'),
        ])

    keyboard.append([
        InlineKeyboardButton(f'{course.name} {back_icon}', callback_data=f'{COURSE} {course.id}'),
        InlineKeyboardButton(
            f"{language['back_to_courses']}".capitalize(),
            callback_data=SUBJECT_LIST),
    ])

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(
        text=f"{language['genitive'](course.name, language['indifinite_exams'])}".capitalize(),
        reply_markup=reply_markup
    )
    return STAGE_THREE