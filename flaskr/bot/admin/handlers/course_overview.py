from flaskr.bot.utils.is_admin import is_admin
from flaskr import db
from flaskr.models import Course, User
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update, ReplyKeyboardRemove
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from flaskr.bot.admin.admin_constants import COURSE_OPTIONS, RECIEVE_NEW_COURSE


def course_overview(update: Update, context: CallbackContext, course_name=None) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    course_name = course_name if course_name else update.message.text

    course = session.query(Course).filter(Course.ar_name==course_name).one()

    # write to chat data
    context.chat_data['course_id'] = course.id

    reply_keyboard = []
    reply_keyboard.append(['المحاضرات', 'المراجع', 'الامتحانات'])
    reply_keyboard.append(['تعديل الاسم', 'تعديل الرمز'])
    reply_keyboard.append(['حذف المادة'])
    reply_keyboard.append(['رجوع'])
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(f'{course.ar_name}',
            reply_markup=markup,
    )

    session.close()
    return COURSE_OPTIONS


def to_course_overview(update: Update, context: CallbackContext) -> int:
    session = db.session


    if not is_admin(update, context, session):
        return

    # reads from context
    course_id = context.chat_data['course_id']

    course = session.query(Course).filter(Course.id==course_id).one()
    course_name = course.ar_name
    session.close()
    return course_overview(update, context, course_name=course_name)


def add_course(update: Update, context: CallbackContext) -> int:
    session = db.session


    if not is_admin(update, context, session):
        return

    update.message.reply_text('''ادخل اسم ورمز المادة على الشكل:
    الاسم: اسم المادة [- الاسم بالنجليزية]
    الرمز: رمز المادة
    مثال:
    الاسم: فيزياء نووية
    الرمز: فيز101''', reply_markup=ReplyKeyboardRemove())

    session.close()
    return RECIEVE_NEW_COURSE
