from flaskr.bot.utils.get_current_semester import get_current_semester
from flaskr.bot.utils.is_admin import is_admin
from flaskr import db
from flaskr.models import Course, Semester
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
import logging
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup 
from flaskr.bot.admin.admin_constants import COURSE_LIST

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def admin_handler(update: Update, context: CallbackContext) -> int:

    user = update.message.from_user
    logger.info("Admin %s started the conversation.", user.first_name)

    session = db.session

    if not is_admin(update, context, session):
        return

    if 'semester_id' in context.chat_data:
        del context.chat_data['semester_id']

    if 'course_id' in context.chat_data:
        del context.chat_data['course_id']

    current_semester = get_current_semester(session)

    courses =  session.query(Course) \
        .join(Semester, Semester.id == Course.semester_id, isouter=True) \
        .filter(( Semester.id==current_semester.semester_id ) | ( Course.semester_id==None )) \
        .order_by(Course.semester_id.desc(), Course.id).all()

    reply_keyboard = []

    for course in courses:
        reply_keyboard.append([
            course.ar_name
        ])

    markup = ReplyKeyboardMarkup(
        reply_keyboard,
        resize_keyboard=True,
        input_field_placeholder='اختر مادة'
        ) if len(reply_keyboard) > 1 else ReplyKeyboardRemove()


    semester_name = ' - لا يوجد سمستر حالي'

    if current_semester.semester:
        semester_name = f' - سمستر {current_semester.semester.number}'

    update.message.reply_text(
        f'Admin {user.first_name}{semester_name}',
        reply_markup=markup,
    )

    session.close()
    return COURSE_LIST
