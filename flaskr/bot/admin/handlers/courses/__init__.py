from flaskr.bot.utils.is_admin import is_admin
from flaskr import db
from flaskr.models import Course, User
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update, ReplyKeyboardRemove
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from flaskr.bot.admin.admin_constants import COURSE_OPTIONS, RECIEVE_NEW_COURSE


def back_from_edit_course(update: Update, context: CallbackContext) -> int:
    handler = context.chat_data['back_from_edit_course']
    return handler(update, context)

def edit_course(update: Update, context: CallbackContext, course_name=None) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    course = None

    if update.message.text == 'رجوع':
        course = session.query(Course).filter(Course.id==context.chat_data['course_id']).one()
    
    else:
        course_name = course_name if course_name else update.message.text

        course = session.query(Course).filter(Course.ar_name==course_name).one()


    # write to chat data
    context.chat_data['course_id'] = course.id

    course_semester = 'N/A' if course.semester is None else course.semester.number

    reply_keyboard = []
    reply_keyboard.append(['المحاضرات', 'المراجع', 'اللابات'])
    reply_keyboard.append(['الامتحانات'])
    reply_keyboard.append(['تعديل الاسم', 'تعديل الرمز'])
    reply_keyboard.append(['حذف المادة', f'سمستر: {course_semester}'])
    reply_keyboard.append(['رجوع'])
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(f'{course.ar_name}',
            reply_markup=markup,
    )

    session.close()
    return COURSE_OPTIONS


def to_edit_course(update: Update, context: CallbackContext) -> int:
    session = db.session


    if not is_admin(update, context, session):
        return

    # reads from context
    course_id = context.chat_data['course_id']

    course = session.query(Course).filter(Course.id==course_id).one()
    course_name = course.ar_name
    session.close()
    return edit_course(update, context, course_name=course_name)


def add_course(update: Update, context: CallbackContext) -> int:
    session = db.session


    if not is_admin(update, context, session):
        return

    update.message.reply_text('''ادخل اسم ورمز المادة على الشكل:
    الاسم: اسم المادة [- الاسم بالانجليزية]
    الرمز: رمز المادة [- رمز المادة بالانجليزية]
    مثال:
    الاسم: فيزياء نووية
    الرمز: فيز101''', reply_markup=ReplyKeyboardRemove())

    session.close()
    return RECIEVE_NEW_COURSE
