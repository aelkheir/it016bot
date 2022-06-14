from flaskr.bot.user.handlers.start_over import start_over
from flaskr.bot.utils.get_current_semester import get_current_semester
from flaskr.bot.utils.get_user_language import get_user_language
from flaskr.bot.utils.user_required import user_required
import logging
from flaskr.models import Course, Semester, User
from flaskr import db
from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from flaskr.bot.user.user_constants import   COURSE, COURSE_OVERVIEW


logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update: Update, context: CallbackContext) -> int:
    """Send message on `/start`."""
    session = db.session

    from_user = update.message.from_user
    logger.info("User %s started the conversation.", from_user.first_name)

    # delete from context
    if 'user_semester_id' in context.chat_data:
        del context.chat_data['user_semester_id']
    if 'user_semester_number' in context.chat_data:
        del context.chat_data['user_semester_number']

    user = user_required(update, context, session)
    language = get_user_language(context.chat_data['language'])

    user = session.query(User).filter(User.id==user.id).one()

    user.start_count += 1

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

    update.message.reply_text(
        f'{language["courses"]}:'.capitalize(),
        reply_markup=reply_markup
    )

    session.commit()
    session.close()
