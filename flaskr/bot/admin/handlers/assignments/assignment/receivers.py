import re
from flaskr import db
from flaskr.bot.admin.handlers.assignments import list_assignment_files
from flaskr.models import  Assignment, Document, Lab, Photo, Video, YoutubeLink
from telegram.ext import CallbackContext
from telegram import Update, ReplyKeyboardMarkup
from flaskr.bot.admin.handlers.labs import list_lab_files
from flaskr.bot.utils.is_admin import is_admin
from flaskr.bot.admin.admin_constants import RECIEVE_LAB_NUMBER, RECIEVIE_ASSIGNMENT_FILE,  RECIEVIE_LAB_FILE
from flaskr.bot.utils.youtube import get_youtube_video
from flaskr.bot.utils.is_admin import is_admin


def recieve_assignment_number(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    # reads from context
    assignment_id = context.chat_data['assignment_id']

    number_regex = re.compile(f'\d+')
    number_match = number_regex.search(update.message.text)

    if number_match:
        assignment = session.query(Assignment).filter(Assignment.id==assignment_id).one()
        assignment.assignment_number = number_match.group()
        session.commit()
        session.close()
        return list_assignment_files(update, context, assignment_id=assignment_id)

    else:
        update.message.reply_text(f'''الرجاء ادخال رقم اللاب مباشرة، مثال:
        3''' )
        return RECIEVE_LAB_NUMBER



def recieve_assignment_file(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    reply_keyboard = []

    reply_keyboard.append(['رجوع'])

    markup = ReplyKeyboardMarkup(keyboard=reply_keyboard, resize_keyboard=True)

    # reads from context
    assignment_id = context.chat_data['assignment_id']

    assignment = session.query(Assignment).filter(Assignment.id==assignment_id).one()

    file_name = ''
    inserted = False

    if update.message.document:
        file = update.message.document
        file_name = file.file_name if file.file_name else file.file_unique_id + ' [document]'
        document = Document(
            file_name=file.file_name,
            file_id=file.file_id,
            file_unique_id=file.file_unique_id,
        )
        document.assignment = assignment
        session.add(document)
        inserted = True

    elif update.message.photo:
        # use file_unique_id as file_name
        file = update.message.photo[-1]
        file_name = file.file_unique_id + ' [photo]'

        photo = Photo(
            file_name=file_name,
            file_id=file.file_id,
            file_unique_id=file.file_unique_id,
        )
        photo.assignment = assignment
        session.add(photo)
        inserted = True

    if inserted:
        session.commit()
        session.close()
        update.message.reply_text(f'تمت اضافة {file_name}', reply_markup=markup)

    else :
        update.message.reply_text(f'حدث خطا الرجاء ارسال ملف document او photo', reply_markup=markup)
    
    return RECIEVIE_ASSIGNMENT_FILE

