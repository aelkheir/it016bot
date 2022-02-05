from telegram.files.photosize import PhotoSize
from telegram.files.document import Document
from flaskr.bot.admin.admin_constants import RECIEVE_EXAM_FILE
from flaskr.bot.utils.is_admin import is_admin
from flaskr import db
from flaskr.models import  Exam, Photo, Document as MyDocument
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update, ReplyKeyboardMarkup


def recieve_exam_file(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    reply_keyboard = []

    reply_keyboard.append(['رجوع'])

    markup = ReplyKeyboardMarkup(keyboard=reply_keyboard, resize_keyboard=True)

    file = None

    message = update.message

    if message.document:
        file = message.document

    elif message.photo:
        file = message.photo[-1]

    # reads from context
    exam_id = context.chat_data['exam_id']

    exam = session.query(Exam).filter(Exam.id==exam_id).one()

    if isinstance(file, Document):
        document = MyDocument(
            file_name=file.file_name,
            file_id=file.file_id,
            file_unique_id=file.file_unique_id,
        )
        document.exam = exam
        session.add(document)
        update.message.reply_text(f'تم اضافة {file.file_name}', reply_markup=markup)

    elif isinstance(file, PhotoSize):
        # user file_unique_id as file_name
        file_name = file.file_unique_id + ' [photo]'

        photo = Photo(
            file_name=file_name,
            file_id=file.file_id,
            file_unique_id=file.file_unique_id,
        )
        photo.exam = exam
        session.add(photo)
        update.message.reply_text(f'تم اضافة {file_name}', reply_markup=markup)


    session.commit()
    session.close()
    return RECIEVE_EXAM_FILE
    