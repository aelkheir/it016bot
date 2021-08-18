from flaskr.bot.utils.is_owner import is_owner
import math
from flaskr.bot.owner.owner_constants import ADMINS_LIST, USER_VIEW
from flaskr import db
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update, ReplyKeyboardMarkup
from flaskr.models import User



def list_users(update: Update, context: CallbackContext) -> int:

    session = db.session

    if not is_owner(update, context, session):
        return

    if 'viewed_user_id' in context.chat_data:
        del context.chat_data['viewed_user_id']

    users = session.query(User).all()

    reply_keyboard = []

    reply_keyboard.append([f'العدد الكلي: {len(users)}'])

    for row_index in range(0, math.ceil(len(users) / 2)):
        row = []
        is_row_full = len(users) // 2 >= row_index + 1
        row_size = 2 if is_row_full else len(users) % 2
        row_start = row_index * 2
        for lecture_index in range(row_start, row_start + row_size):
            user = users[lecture_index]
            row.append( f'{user.id} {user.first_name} {user.last_name if user.last_name else ""}')
        reply_keyboard.append(row)

    
    reply_keyboard.append(['رجوع'])

    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

    update.message.reply_text('المستخدمين', reply_markup=markup)
    return USER_VIEW

def list_admins(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_owner(update, context, session):
        return

    if 'viewed_user_id' in context.chat_data:
        del context.chat_data['viewed_user_id']

    admins = session.query(User).filter(User.is_admin==True).all()

    reply_keyboard = []


    for admin in admins:
        reply_keyboard.append([f'{admin.id} {admin.first_name} {admin.last_name if admin.last_name else ""}'])
    
    reply_keyboard.append(['رجوع', 'اضافة مدير'])

    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

    update.message.reply_text('المدراء', reply_markup=markup)

    return ADMINS_LIST