from flaskr.bot.utils.get_current_semester import get_current_semester
from flaskr.bot.utils.get_user_language import get_user_language
from flaskr.bot.utils.user_required import user_required
import logging
from flaskr.models import Course, Semester
from flaskr import db
from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from flaskr.bot.user.user_constants import   COURSE, COURSE_OVERVIEW


logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start_over(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)
    language = get_user_language(context.chat_data['language'])

    current_semester = get_current_semester(session)

    courses =  session.query(Course) \
        .join(Semester, Semester.id == Course.semester_id) \
        .filter((Semester.id==current_semester.semester_id )) \
        .order_by(Course.id).all()

    # temeporarly allow loqman to accses semester 7
    # dlelete if block later
    if user.telegram_id == '1294118831':
        courses = session.query(Course) \
        .join(Semester, Semester.id == Course.semester_id) \
        .filter((Semester.number== 7 )) \
        .order_by(Course.id).all()

    keyboard = []


    for course in courses:
        course_name = course.ar_name \
            if user.language == 'ar' \
            else course.en_name
        course_name = course_name if course_name else course.ar_name

        keyboard.append([
            InlineKeyboardButton(f'{course_name} ({len(course.lectures)})',
            callback_data=f'{COURSE} {course.id}'),
        ])

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(
        f'{language["courses"]}:'.capitalize(),
        reply_markup=reply_markup
    )

    session.close()
    return COURSE_OVERVIEW