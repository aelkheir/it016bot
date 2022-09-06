from flaskr.bot.notifications.notifications_constants import NOTIFICATIONS_SETTINGS
from flaskr.bot.user.user_constants import ARCHIVE, ASSIGNMENTS, COURSE, LABS, SEMESTER, SUBJECT_LIST, TUTORIALS
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

def back_to_tutorials_button(language, user_language, course_id):

    ar_tutorials = language['tutorials'][1:]

    text = [
        back_icon, 
        f"{language['back_to']}".capitalize() +
        f"{' ' + language['tutorials'] if user_language == 'en' else ar_tutorials}".title(),
    ]

    return InlineKeyboardButton(
        ' '.join(text),
        callback_data=f"{course_id} {TUTORIALS}"
    )


def back_to_assignments_button(language, user_language, course_id):

    ar_assignments = language['assignments'][1:]

    text = [
        back_icon, 
        f"{language['back_to']}".capitalize() +
        f"{' ' + language['assignments'] if user_language == 'en' else ar_assignments}".title(),
    ]

    return InlineKeyboardButton(
        ' '.join(text),
        callback_data=f"{course_id} {ASSIGNMENTS}"
    )

def back_to_notification_settings(language, user_language):
    ar_notifications = language['notifications'][1:]

    text = [
        back_icon, 
        f"{language['back_to']}".capitalize() +
        f"{' ' + language['notifications'] if user_language == 'en' else ar_notifications}".title(),
    ]

    return InlineKeyboardButton(
        ' '.join(text),
        callback_data=f"{NOTIFICATIONS_SETTINGS}"
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

def back_to_semester(language, user_language, semester_id, semester_number):

    text = [
        back_icon, 
        f"{language['back_to']}".capitalize() +
        f"{' ' + language['semester'] if user_language == 'en' else language['semester']} {semester_number}".title(),
    ]

    return InlineKeyboardButton(
        ' '.join(text),
        callback_data=f'{SEMESTER} {semester_id} {semester_number}'
    )

