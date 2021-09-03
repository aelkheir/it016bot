from flaskr.bot.utils.buttons import back_to_courses_button
from flaskr.bot.utils.user_required import user_required
import math
from flaskr.models import Course, Lecture
from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from flaskr.bot.user.user_constants import ALL, EXAMS, LECTURES, REFFERENCES, STAGE_TWO
from flaskr import db


back_icon = '»'


def course_overview(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)
    language = context.chat_data['language']

    _, course_id = query.data.split(' ')

    course = session.query(Course).filter(Course.id == course_id).one()

    lectures = session.query(Lecture)\
        .filter(Lecture.course_id == course_id)\
        .order_by(Lecture.lecture_number).all()

    keyboard = []

    for row_index in range(0, math.ceil(len(lectures) / 3)):
        row = []
        is_row_full = len(lectures) // 3 >= row_index + 1
        row_size = 3 if is_row_full else len(lectures) % 3
        row_start = row_index * 3

        for lecture_index in range(row_start, row_start + row_size):
            lecture = lectures[lecture_index]
            row.append(InlineKeyboardButton(
                f"{language['lecture']} {lecture.lecture_number}".capitalize(),
                callback_data=f'{course.id} {lecture.id}'),
            )
        keyboard.append(row)
    
    if len(lectures) > 1:
        keyboard.append([
            InlineKeyboardButton(
                f"{language['download']} {language['all']} {language['lectures']}".title(),
                callback_data=f'{LECTURES} {course.id}')
        ])

    refference_exam_row = []

    if len(course.refferences) > 0:
        refference_exam_row.append(
            InlineKeyboardButton(
                f"{language['references']} ({len(course.refferences)})".capitalize(),
                callback_data=f'{course.id} {REFFERENCES}'),
        )

    if len(course.exams) > 0:
        refference_exam_row.append(
            InlineKeyboardButton(
                f"{language['exams']} ({len(course.exams)})".capitalize(),
                callback_data=f'{course.id} {EXAMS}'),
        )

    if len(refference_exam_row) > 0:
        keyboard.append(refference_exam_row)

    keyboard.append([back_to_courses_button(language, user.language)])

    reply_markup = InlineKeyboardMarkup(keyboard)

    if len(course.lectures) == 0 and len(course.refferences) == 0 and len(course.exams) == 0:
        query.edit_message_text(
            text=f"{language['nothing_yet']}.".capitalize(), reply_markup=reply_markup
        )

    else:
        course_name = course.ar_name \
            if user.language == 'ar' \
            else course.en_name
        course_name = course_name if course_name else course.ar_name

        query.edit_message_text(
            text=f"{course_name}:".title(),
            reply_markup=reply_markup
        )

    session.close()
    return STAGE_TWO
