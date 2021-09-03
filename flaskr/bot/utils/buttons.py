from flaskr.bot.user.user_constants import COURSE, SUBJECT_LIST
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update


def back_to_courses_button(language, user_language):

    ar_courses = language['courses'][1:]

    return InlineKeyboardButton(
        f"{language['back_to']}".capitalize() +
        f"{' ' + language['courses'] if user_language == 'en' else ar_courses}".title(),
        callback_data=SUBJECT_LIST
    )

def back_to_course_button(language, user_language, en_course_name, ar_course_name, course_id):

    if ar_course_name.startswith('ال'):
       ar_course_name = ar_course_name[1:]

    en_course_name = en_course_name if en_course_name else ar_course_name

    return InlineKeyboardButton(
        f"{language['back_to']}".capitalize() +
        f"{' ' + en_course_name.title() if user_language == 'en' else ar_course_name}".title(),
        callback_data=f'{COURSE} {course_id}'
    )