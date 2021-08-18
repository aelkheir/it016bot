from flaskr.bot.utils.user_required import user_required
import math
from flaskr.models import Course, Lecture
from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from flaskr.bot.user.user_constants import ALL, EXAMS, LECTURES, REFFERENCES, STAGE_TWO, SUBJECT_LIST
from flaskr import db


back_icon = '»'


def course_overview(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user_required(update, context, session)

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
            row.append(
                InlineKeyboardButton(
                    f'المحاضرة {lecture.lecture_number}', callback_data=f'{course.id} {lecture.id}'),
            )
        keyboard.append(row)
    
    if len(lectures) > 1:
        keyboard.append([
            InlineKeyboardButton(f'تحميل جميع المحاضرات',
                                 callback_data=f'{LECTURES} {course.id}')
        ])

    refference_exam_row = []

    if len(course.refferences) > 0:
        refference_exam_row.append(
            InlineKeyboardButton(
                f'المراجع ({len(course.refferences)})', callback_data=f'{course.id} {REFFERENCES}'),
        )

    if len(course.exams) > 0:
        refference_exam_row.append(
            InlineKeyboardButton(
                f'الامتحانات ({len(course.exams)})', callback_data=f'{course.id} {EXAMS}'),
        )

    if len(refference_exam_row) > 0:
        keyboard.append(refference_exam_row)

    keyboard.append([
        InlineKeyboardButton(
            f'قائمة المواد {back_icon}', callback_data=SUBJECT_LIST),
    ])

    reply_markup = InlineKeyboardMarkup(keyboard)

    if len(course.lectures) == 0 and len(course.refferences) == 0 and len(course.exams) == 0:
        query.edit_message_text(
            text=f"لا شيء بعد.", reply_markup=reply_markup
        )

    else:
        query.edit_message_text(
            text=f"{course.name}", reply_markup=reply_markup
        )

    session.close()
    return STAGE_TWO
