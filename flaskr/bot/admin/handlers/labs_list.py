import re
from flaskr.bot.utils.is_admin import is_admin
from flaskr.bot.admin.admin_constants import LAB_OPTIONS, LECTURE_OPTIONS
from flaskr import db
from flaskr.models import Course, Lab, Lecture
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update 
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from flaskr.bot.admin.handlers.course_options import list_labs


def list_lab_files(update: Update, context: CallbackContext, lab_id=None) -> int:

    if 'file_name' in context.chat_data:
        del context.chat_data['file_name']

    session = db.session

    if not is_admin(update, context, session):
        return

    if 'lab_id' in context.chat_data and not lab_id:
        lab_id = context.chat_data['lab_id']

    if not lab_id:
        lab_id_regex = re.compile('\(id: (\d+)\)')
        lab_id_match = lab_id_regex.search(update.message.text)
        lab_id = lab_id_match.groups()[0]

    if lab_id:
        # write to context
        context.chat_data['lab_id'] = lab_id

    # reads from context

    lab = session.query(Lab).filter(Lab.id==int(lab_id)).one()
        

    reply_keyboard = []

    for document in lab.documents:
        reply_keyboard.append([f'{document.file_name}'])

    for video in lab.videos:
        reply_keyboard.append([f'{video.file_name}'])
    
    for youtube_link in lab.youtube_links:
        reply_keyboard.append([f'{youtube_link.video_title}'])

    reply_keyboard.append(['اضافة ملف'])
    reply_keyboard.append(['حذف اللاب', f'تعديل رقم اللاب: {lab.lab_number}'])
    reply_keyboard.append(['رجوع'])

    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text(f'{lab.course.ar_name}: لاب رقم {lab.lab_number}',
            reply_markup=markup,
    )

    session.close()
    return LAB_OPTIONS


def to_list_lab_files(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    # read from context
    lecture_id = context.chat_data['lecture_id']

    session.close()
    return list_lab_files(update, context, lecture_id=lecture_id)

def add_lab(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    # reads from context
    course_id = context.chat_data['course_id']

    course = session.query(Course).filter(Course.id==course_id).one()
    new_lab = Lab(lab_number=len(course.labs)+1)
    new_lab.course = course
    session.add(new_lab)

    update.message.reply_text(f'تمت اضافة لاب جديد بنجاح')

    session.commit()
    session.close()
    return list_labs(update, context)