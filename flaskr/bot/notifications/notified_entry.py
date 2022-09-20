import math
import re
from flaskr.bot.notifications.notifications_constants import LAB_NOTIFICATION_MESSAGE, LECTURE_NOTIFICATION_MESSAGE, NOTIFIED_LAB_OPTIONS, NOTIFIED_LECTURE_OPTIONS, NOTIFIED_TUTORIAL_OPTIONS, TUTORIAL_NOTIFICATION_MESSAGE
from flaskr.bot.utils.buttons import back_to_course_button
from flaskr.bot.utils.get_user_language import get_user_language
from flaskr.bot.utils.user_required import user_required
from flaskr.models import Lab, Lecture, Tutorial
from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, constants
from flaskr.bot.user.user_constants import  FILE, LAB, LECTURE, SHOW_GLOBAL_NOTE, TUTORIAL
from flaskr import db

back_icon ='»'

course_regex = re.compile(r'\+c\+')
number_regex = re.compile(r'\+n\+')

def list_notified_lecture_files(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)
    language = get_user_language(context.chat_data['language'])

    _, lecture_id = query.data.split(' ')

    lecture = session.query(Lecture).filter(Lecture.id==lecture_id).one()
    course = lecture.course

    keyboard = []

    for document in lecture.documents:
        keyboard.append([
            InlineKeyboardButton(
                f'{document.file_name}',
                callback_data=f'{FILE} {document.id} {document.file_unique_id}'
            )
        ])

    for video in lecture.videos:
        keyboard.append([
            InlineKeyboardButton(
                f'{video.file_name}',
                callback_data=f'{FILE} {video.id} {video.file_unique_id}'
            )
        ])

    for youtube_link in lecture.youtube_links:
        keyboard.append([
            InlineKeyboardButton(f'{youtube_link.video_title}',
            callback_data=f'{FILE} {youtube_link.id}')
        ])

    if len(lecture.documents) + len(lecture.videos) + len(lecture.youtube_links) > 1:
        keyboard.append([InlineKeyboardButton(
            f"{language['download']} {language['all']} {language['files']}".title(),
            callback_data=f'{LECTURE} {lecture.id}')
        ])

    keyboard.append([
        InlineKeyboardButton(
                f"{language['hide']}".capitalize(),
                callback_data=f'{LECTURE_NOTIFICATION_MESSAGE} {lecture_id}'
            )
    ])

    course_name = course.ar_name \
        if user.language == 'ar' \
        else course.en_name
    course_name = course_name if course_name else course.ar_name

    template = language['notify_lecture_template']
    message = re.sub(course_regex, course_name, template)
    message = '🔔  ' + re.sub(number_regex, f'{lecture.lecture_number}', message)

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=f"{message}",
        reply_markup=reply_markup,
        parse_mode=constants.PARSEMODE_MARKDOWN_V2
    )

    session.close()
    return NOTIFIED_LECTURE_OPTIONS

def list_notified_lab_files(update: Update, context: CallbackContext) -> int:
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

    keyboard.append([
        InlineKeyboardButton(
                f"{language['hide']}".capitalize(),
                callback_data=f'{LAB_NOTIFICATION_MESSAGE} {lab_id}'
            )
    ])

    course_name = course.ar_name \
        if user.language == 'ar' \
        else course.en_name
    course_name = course_name if course_name else course.ar_name

    template = language['notify_lab_template']
    message = re.sub(course_regex, course_name, template)
    message = '🔔  ' + re.sub(number_regex, f'{lab.lab_number}', message)

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=f"{message}",
        reply_markup=reply_markup,
        parse_mode=constants.PARSEMODE_MARKDOWN_V2
    )

    session.close()
    return NOTIFIED_LAB_OPTIONS

def list_notified_tutorial_files(update: Update, context: CallbackContext) -> int:
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

    keyboard.append([
        InlineKeyboardButton(
                f"{language['hide']}".capitalize(),
                callback_data=f'{TUTORIAL_NOTIFICATION_MESSAGE} {tutorial_id}'
            )
    ])

    course_name = course.ar_name \
        if user.language == 'ar' \
        else course.en_name
    course_name = course_name if course_name else course.ar_name

    template = language['notify_tutorial_template']
    message = re.sub(course_regex, course_name, template)
    message = '🔔  ' + re.sub(number_regex, f'{tutorial.tutorial_number}', message)

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=f"{message}",
        reply_markup=reply_markup,
        parse_mode=constants.PARSEMODE_MARKDOWN_V2
    )

    session.close()
    return NOTIFIED_TUTORIAL_OPTIONS
