from flaskr.bot.user.handlers.archive import list_semesters
from flaskr.bot.utils.buttons import back_to_archive_button
from flaskr.bot.utils.get_current_semester import get_current_semester
from flaskr.bot.utils.get_user_language import get_user_language
from flaskr.bot.utils.user_required import user_required
import logging
from flaskr.models import Course, Semester, User
from flaskr import db
from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from flaskr.bot.user.user_constants import   ARCHIVED_SEMESTER, COURSE, COURSE_OVERVIEW



def list_semester_courses(
    update: Update, context: CallbackContext,
    semester_id=None, semester_number=''
    ) -> int:
    """Send message on `/start`."""
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)
    language = get_user_language(context.chat_data['language'])


    if not semester_id:
        _, semester_id, semester_number = query.data.split(' ')


    # wirite to context
    context.chat_data[f'{update.effective_message.message_id} user_semester_id'] = semester_id
    context.chat_data[f'{update.effective_message.message_id} user_semester_number'] = semester_number

    # wirite to context
    context.chat_data[f"{update.effective_message.message_id} from_archive"] = True



    courses =  session.query(Course) \
        .join(Semester, Semester.id == Course.semester_id) \
        .filter((Semester.id==semester_id )) \
        .order_by(Course.id).all()

    keyboard = []

    for course in courses:
        course_name = course.ar_name \
            if user.language == 'ar' \
            else course.en_name
        course_name = course_name if course_name else course.ar_name

        keyboard.append([
            InlineKeyboardButton(f'{course_name}',
            callback_data=f'{COURSE} {course.id}'),
        ])

    keyboard.append([back_to_archive_button(language, user.language)])

    reply_markup = InlineKeyboardMarkup(keyboard)


    query.edit_message_text(
        f'{language["semester"]} {semester_number}:'.capitalize(),
        reply_markup=reply_markup
    )

    session.commit()
    session.close()
    return ARCHIVED_SEMESTER

