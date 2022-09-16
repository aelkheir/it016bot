from flaskr.bot.user.handlers.start_over import start_over
from flaskr.bot.utils.get_current_semester import get_current_semester
from flaskr.bot.utils.get_user_language import get_user_language
from flaskr.bot.utils.user_required import user_required
import logging
from flaskr.models import Course, Semester, User
from flaskr import db
from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, constants
from flaskr.bot.user.user_constants import   COURSE, COURSE_OVERVIEW, SHOW_GLOBAL_NOTE


logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update: Update, context: CallbackContext) -> int:
    """Send message on `/start`."""
    session = db.session

    from_user = update.message.from_user
    logger.info("User %s started the conversation.", from_user.first_name)

    user = user_required(update, context, session)
    language = get_user_language(context.chat_data['language'])

    user = session.query(User).filter(User.id==user.id).one()

    user.start_count += 1

    current_semester = get_current_semester(session)

    courses =  session.query(Course) \
        .join(Semester, Semester.id == Course.semester_id) \
        .filter((Semester.id==current_semester.semester_id )) \
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

    reply_markup = InlineKeyboardMarkup(keyboard)

    show_note = SHOW_GLOBAL_NOTE and bool(course.semester.current)

    update.message.reply_text(
        f'{language["courses"]}'.capitalize() \
        +  (f"{language['global_note']}" if show_note else ''),
        reply_markup=reply_markup,
        parse_mode=constants.PARSEMODE_MARKDOWN_V2
    )

    session.commit()
    session.close()

    return COURSE_OVERVIEW
