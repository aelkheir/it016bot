import math
from flaskr.bot.utils.get_current_semester import get_current_semester
from flaskr.bot.utils.user_required import user_required
import logging
from flaskr.models import Course, Semester, User
from flaskr import db
from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from flaskr.bot.user.user_constants import   COURSE, COURSE_OVERVIEW, SEMESTER, SEMESTER_LIST


def list_semesters(update: Update, context: CallbackContext) -> int:
    """Send message on `/start`."""
    session = db.session


    query = update.callback_query
    if query:
        query.answer()

    user = user_required(update, context, session)
    language = context.chat_data['language']

    user = session.query(User).filter(User.id==user.id).one()

    user.start_count += 1

    current_semester = get_current_semester(session)

    if not current_semester.semester_id and update.message:
      update.message.reply_text(
          f'{language["nothing_yet"]}'.capitalize(),
      )
      return None

    semesters =  session.query(Semester) \
      .filter(Semester.id < current_semester.semester_id) \
      .order_by(Semester.number).all()

    reply_keyboard = []

    for row_index in range(0, math.ceil(len(semesters) / 2)):
        row = []
        is_row_full =  len(semesters) // 2 >= row_index + 1
        row_size = 2 if is_row_full else len(semesters) % 2
        row_start = row_index * 2

        for semester_index in range(row_start, row_start + row_size):
            semester = semesters[semester_index]
            row.append(
                InlineKeyboardButton(f"{language['semester']} {semester.number}".title(),
                callback_data=f'{SEMESTER} {semester.id} {semester.number}'),
            )

        reply_keyboard.append(row)

    reply_markup = InlineKeyboardMarkup(reply_keyboard)

    if query:
        query.edit_message_text(
        f'{language["archive"]}:'.capitalize(),
        reply_markup=reply_markup
        )

    elif update.message:
      update.message.reply_text(
          f'{language["archive"]}:'.capitalize(),
          reply_markup=reply_markup
      )

    session.commit()
    session.close()
    return SEMESTER_LIST
