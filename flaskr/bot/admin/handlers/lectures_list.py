import re
from flaskr.bot.utils.is_admin import is_admin
from flaskr.bot.admin.admin_constants import LECTURE_OPTIONS
from flaskr import db
from flaskr.models import Course, Lecture
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update 
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from flaskr.bot.admin.handlers.course_options import list_lectures


def list_files(update: Update, context: CallbackContext, lecture_id=None) -> int:

    if 'file_name' in context.chat_data:
        del context.chat_data['file_name']

    session = db.session

    if not is_admin(update, context, session):
        return

    if 'lecture_id' in context.chat_data and not lecture_id:
        lecture_id = context.chat_data['lecture_id']

    if not lecture_id:
        lecture_id_regex = re.compile('\(id: (\d+)\)')
        lecture_id_match = lecture_id_regex.search(update.message.text)
        lecture_id = lecture_id_match.groups()[0]

    if lecture_id:
        # write to context
        context.chat_data['lecture_id'] = lecture_id

    # reads from context

    lecture = session.query(Lecture).filter(Lecture.id==int(lecture_id)).one()
        

    reply_keyboard = []

    for document in lecture.documents:
        reply_keyboard.append([f'{document.file_name}'])

    for video in lecture.videos:
        reply_keyboard.append([f'{video.file_name}'])
    
    for youtube_link in lecture.youtube_links:
        reply_keyboard.append([f'{youtube_link.video_title}'])

    reply_keyboard.append(['اضافة ملف'])
    reply_keyboard.append(['حذف المحاضرة', f'تعديل رقم المحاضرة: {lecture.lecture_number}'])
    reply_keyboard.append(['رجوع'])

    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(f'{lecture.course.ar_name} {lecture.lecture_number}',
            reply_markup=markup,
    )

    session.close()
    return LECTURE_OPTIONS


def to_list_files(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    # read from context
    lecture_id = context.chat_data['lecture_id']

    session.close()
    return list_files(update, context, lecture_id=lecture_id)

def add_lecture(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    # reads from context
    course_id = context.chat_data['course_id']

    course = session.query(Course).filter(Course.id==course_id).one()
    new_lecture = Lecture(lecture_number=len(course.lectures)+1)
    new_lecture.course = course
    session.add(new_lecture)

    update.message.reply_text(f'تمت اضافة محاضرة جديدة بنجاح')

    session.commit()
    session.close()
    return list_lectures(update, context)