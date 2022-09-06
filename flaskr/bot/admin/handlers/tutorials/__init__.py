import re
from sqlalchemy import func
from flaskr.bot.utils.is_admin import is_admin
from flaskr.bot.admin.admin_constants import LAB_OPTIONS, TUTORIAL_OPTIONS
from flaskr import db
from flaskr.models import Course, Lab, Tutorial
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update 
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from flaskr.bot.admin.handlers.courses.course import list_labs


def list_tutorial_files(update: Update, context: CallbackContext, tutorial_id=None) -> int:

    if 'file_name' in context.chat_data:
        del context.chat_data['file_name']

    session = db.session

    if not is_admin(update, context, session):
        return

    if not tutorial_id and 'tutorial_id' in context.chat_data:
        tutorial_id = context.chat_data['tutorial_id']

    elif not tutorial_id:
        tutorial_id_regex = re.compile('\(id: (\d+)\)')
        tutorial_id_match = tutorial_id_regex.search(update.message.text)
        tutorial_id = tutorial_id_match.groups()[0]
        # write to context
        context.chat_data['tutorial_id'] = tutorial_id

    elif tutorial_id:
        # write to context
        context.chat_data['tutorial_id'] = tutorial_id

    tutorial = session.query(Tutorial).filter(Tutorial.id==int(tutorial_id)).one()

    reply_keyboard = []

    for document in tutorial.documents:
        reply_keyboard.append([f'{document.file_name}'])

    for video in tutorial.videos:
        reply_keyboard.append([f'{video.file_name}'])
    
    for youtube_link in tutorial.youtube_links:
        reply_keyboard.append([f'{youtube_link.video_title}'])

    reply_keyboard.append(['اضافة ملف', 'نشر'])
    reply_keyboard.append(['حذف التمرين', f'تعديل رقم التمرين: {tutorial.tutorial_number}'])
    reply_keyboard.append(['رجوع'])

    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(f'{tutorial.course.ar_name}: تمرين رقم {tutorial.tutorial_number}',
            reply_markup=markup,
    )

    session.close()
    return TUTORIAL_OPTIONS


def to_list_lab_files(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    # read from context
    lecture_id = context.chat_data['lecture_id']

    session.close()
    return list_tutorial_files(update, context, lecture_id=lecture_id)

def add_tutorial(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    # reads from context
    course_id = context.chat_data['course_id']

    course = session.query(Course).filter(Course.id==course_id).one()

    last_tutorial = session.query(func.max(Tutorial.tutorial_number)) \
      .filter_by(course_id=course_id).first()
    tutorial_number = last_tutorial[0] + 1 if last_tutorial[0] else 1

    new_tutorial = Tutorial(tutorial_number=tutorial_number, published=False)
    new_tutorial.course = course

    session.add(new_tutorial)
    session.commit()

    tutorial_id = new_tutorial.id

    update.message.reply_text(f'تمت اضافة تمرين جديد بنجاح')

    session.close()
    return list_tutorial_files(update, context, tutorial_id=tutorial_id)