from flaskr.bot.utils.is_admin import is_admin
from flaskr.bot.admin.admin_constants import ASSIGNMENT_FILE_OPTIONS,  RECIEVE_ASSIGNMENT_NUMBER, RECIEVIE_ASSIGNMENT_FILE
from flaskr import db
from flaskr.models import  Assignment
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup
from flaskr.bot.admin.handlers.courses.course import list_assignments


def delete_assignment(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    # reads from context
    assignment_id = context.chat_data['assignment_id']

    assignment = session.query(Assignment).filter(Assignment.id==assignment_id).one()
    session.delete(assignment)

    update.message.reply_text(
        f'تم حذف {assignment.course.ar_name} لاب رقم {assignment.assignment_number}'
    )

    session.commit()
    session.close()
    return list_assignments(update, context)


def edit_assignment_number(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    update.message.reply_text(f'''ادخل رقم التسليم مباشرة، مثال:
    3''', reply_markup=ReplyKeyboardRemove())

    session.close()
    return RECIEVE_ASSIGNMENT_NUMBER


def add_file(update: Update, context: CallbackContext) -> int:
    session = db.session

    reply_keyboard = []
    reply_keyboard.append(['رجوع'])
    markup = ReplyKeyboardMarkup(keyboard=reply_keyboard, resize_keyboard=True)

    if not is_admin(update, context, session):
        return

    update.message.reply_text('ارسل ملف document او video او youtube link:', reply_markup=markup)

    session.close()
    return RECIEVIE_ASSIGNMENT_FILE


def edit_file(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    file_name = update.message.text

    # write to context
    context.chat_data['file_name'] = file_name

    reply_keyboard = [
        [ 'عرض' ],
        [ 'حذف الملف' ],
        [ 'رجوع' ]
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

    update.message.reply_text(f'{file_name}', reply_markup=markup)

    session.close()
    return ASSIGNMENT_FILE_OPTIONS