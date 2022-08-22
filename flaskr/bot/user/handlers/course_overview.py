from sqlalchemy import true
from flaskr.bot.utils.buttons import back_to_courses_button, back_to_semester
from flaskr.bot.utils.get_user_language import get_user_language
from flaskr.bot.utils.user_required import user_required
import math
from flaskr.models import Assignment, Course, Lab, Lecture
from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from flaskr.bot.user.user_constants import  ASSIGNMENTS, EXAMS, LABS, LECTURE, LECTURES, REFFERENCES, SHOW_GLOBAL_NOTE, STAGE_TWO
from flaskr import db



def course_overview(update: Update, context: CallbackContext, course_id=None, from_archive=False) -> int:
    session = db.session

    query = update.callback_query
    if not course_id:
        query.answer()

    user = user_required(update, context, session)
    language = get_user_language(context.chat_data['language'])


    if not course_id:
        _, course_id = query.data.split(' ')

    course =  session.query(Course).filter(Course.id == course_id).one()

    lectures = session.query(Lecture)\
        .filter(Lecture.course_id == course_id, Lecture.published==True)\
        .order_by(Lecture.lecture_number).all()

    labs = session.query(Lab)\
        .filter(Lab.course_id == course_id, Lab.published==True).all()

    assignments = session.query(Assignment)\
        .filter(Assignment.course_id == course_id, Assignment.published==True).all()

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
                callback_data=f'{LECTURE} {lecture.id}'),
            )

        if user.language == 'ar':
            row.reverse()

        keyboard.append(row)

    refference_lab_row = []

    if len(course.refferences) > 0:
        refference_lab_row.append(
            InlineKeyboardButton(
                f"{language['references']} ({len(course.refferences)})".capitalize(),
                callback_data=f'{course.id} {REFFERENCES}'),
        )

    if len(labs) > 0:
        refference_lab_row.append(
            InlineKeyboardButton(
                f"{language['labs']} ({len(labs)})".capitalize(),
                callback_data=f'{course.id} {LABS}'
        ))

    if len(refference_lab_row) > 0:
        keyboard.append(refference_lab_row)


    exam_assignment_row = []

    if len(course.exams) > 0:
        exam_assignment_row.append(
            InlineKeyboardButton(
                f"{language['exams']} ({len(course.exams)})".capitalize(),
                callback_data=f'{course.id} {EXAMS}'
            )
        )

    if len(assignments) > 0:
        exam_assignment_row.append(
            InlineKeyboardButton(
                f"{language['assignments']} ({len(assignments)})".capitalize(),
                callback_data=f'{course.id} {ASSIGNMENTS}'
            )
        )

    if len(exam_assignment_row) > 0:
        keyboard.append(exam_assignment_row)

    # mutates from_archive
    if f"{update.effective_message.message_id} from_archive" in context.chat_data:
        from_archive = true

    if not from_archive:
        keyboard.append([back_to_courses_button(language, user.language)])

    elif from_archive:
        # read from context
        semester_id = context.chat_data[f'{update.effective_message.message_id} user_semester_id']
        semester_number = context.chat_data[f'{update.effective_message.message_id} user_semester_number'] 
        keyboard.append([back_to_semester(language, user.language, semester_id, semester_number)])



    reply_markup = InlineKeyboardMarkup(keyboard)

    course_name = course.ar_name \
        if user.language == 'ar' \
        else course.en_name
    course_name = course_name if course_name else course.ar_name

    show_note = SHOW_GLOBAL_NOTE and bool(course.semester.current)

    if update.callback_query:
        query.edit_message_text(
            text=f"{course_name}:" + (f"{language['global_note']}" if show_note else ''),
            reply_markup=reply_markup
        )
    elif update.message:
        update.message.reply_text(
            f"{course_name}:" + (f"{language['global_note']}" if show_note else ''),
            reply_markup=reply_markup
        )

    session.close()
    return STAGE_TWO
