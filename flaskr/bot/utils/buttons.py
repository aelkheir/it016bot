from flaskr.bot.user.user_constants import ARCHIVE, COURSE, LABS, SUBJECT_LIST
from telegram import InlineKeyboardButton


back_icon = '«'


def back_to_courses_button(language, user_language):

    ar_courses = language['courses'][1:]

    text = [
        back_icon, 
        f"{language['back_to']}".capitalize() +
        f"{' ' + language['courses'] if user_language == 'en' else ar_courses}".title(),
    ]

    return InlineKeyboardButton(
        ' '.join(text),
        callback_data=SUBJECT_LIST
    )

def back_to_labs_button(language, user_language, course_id):

    ar_labs = language['labs'][1:]

    text = [
        back_icon, 
        f"{language['back_to']}".capitalize() +
        f"{' ' + language['labs'] if user_language == 'en' else ar_labs}".title(),
    ]

    return InlineKeyboardButton(
        ' '.join(text),
        callback_data=f"{course_id} {LABS}"
    )

def back_to_course_button(language, user_language, en_course_name, ar_course_name, course_id):

    if ar_course_name.startswith('ال'):
       ar_course_name = ar_course_name[1:]

    en_course_name = en_course_name if en_course_name else ar_course_name

    text = [
        back_icon, 
        f"{language['back_to']}".capitalize() +
        f"{' ' + en_course_name if user_language == 'en' else ar_course_name}",
    ]

    return InlineKeyboardButton(
        ' '.join(text),
        callback_data=f'{COURSE} {course_id}'
    )

def back_to_archive_button(language, user_language):

    ar_archive = language['archive'][1:]

    text = [
        back_icon, 
        f"{language['back_to']}".capitalize() +
        f"{' ' + language['archive'] if user_language == 'en' else ar_archive}".title(),
    ]

    return InlineKeyboardButton(
        ' '.join(text),
        callback_data=f"{ARCHIVE}"
    )
