from flaskr.bot.utils.is_admin import is_admin
from flaskr import db
from flaskr.models import Course, User
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update, ReplyKeyboardRemove
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from flaskr.bot.admin.admin_constants import COURSE_OPTIONS, RECIEVE_NEW_COURSE


def edit_course(
    update: Update,
    context: CallbackContext,
    course_name=None,
    from_archive=False
    ) -> int:
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
    reply_keyboard.append(['المحاضرات', 'المراجع']),
    reply_keyboard.append(['اللابات', 'التمارين']),
    reply_keyboard.append(['الامتحانات', 'التساليم'])
    reply_keyboard.append(['الشيتات']),
    reply_keyboard.append(['تعديل الاسم', 'تعديل الرمز'])
    reply_keyboard.append(['حذف المادة', f'سمستر: {course_semester}'])
    if from_archive:
        semester_number = context.chat_data['semester_number']
        reply_keyboard.append([f'رجوع لسمستر {semester_number}'])
    else:
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

    from_archive = False
    # reads from context
    if 'semester_id' in context.chat_data:
        from_archive = True

    # reads from context
    course_id = context.chat_data['course_id']

    course = session.query(Course).filter(Course.id==course_id).one()
    course_name = course.ar_name
    session.close()
    return edit_course(update, context, course_name=course_name, from_archive=from_archive)


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
