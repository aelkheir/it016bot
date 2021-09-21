import time
import math
from telegram.ext import CallbackContext, CallbackContext
from telegram.botcommandscope import  BotCommandScopeChat
from telegram import Update, ReplyKeyboardMarkup
from flaskr.bot.localization import ar, en
from flaskr.bot.utils.is_owner import is_owner
from flaskr.bot.utils.set_bot_commands import get_admin_commands, get_common_commands, get_owner_commands, get_user_commands
from flaskr.bot.owner.owner_constants import ADMINS_LIST, CHOICE, USER_VIEW
from flaskr import db
from flaskr.models import User



def list_users(update: Update, context: CallbackContext) -> int:

    session = db.session

    if not is_owner(update, context, session):
        return

    if 'viewed_user_id' in context.chat_data:
        del context.chat_data['viewed_user_id']

    users = session.query(User).order_by(User.id).all()

    reply_keyboard = []

    reply_keyboard.append([f'عرض الكل: {len(users)}'])

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

    admins = session.query(User).filter(User.is_admin==True).order_by(User.id).all()

    reply_keyboard = []


    for admin in admins:
        reply_keyboard.append([f'{admin.id} {admin.first_name} {admin.last_name if admin.last_name else ""}'])
    
    reply_keyboard.append(['رجوع', 'اضافة مدير'])

    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

    update.message.reply_text('المدراء', reply_markup=markup)

    return ADMINS_LIST

def set_bot_commands(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_owner(update, context, session):
        return
    
    for user in session.query(User).all():
        time.sleep(30)

        user = session.query(User).filter(User.id==user.id).one()

        if not user.chat_id:
            continue

        language = ar\
        if user.language == 'ar'\
        else en

        if not user.is_admin and not user.is_owner:

            update.effective_chat.bot.set_my_commands(
                get_user_commands(language, user.language) + get_common_commands(language),
                scope=BotCommandScopeChat(user.chat_id)
            )

        elif user.is_admin and not user.is_owner:
            
            update.effective_message.bot.set_my_commands(
                get_admin_commands(language, user.language) + get_common_commands(language),
                scope=BotCommandScopeChat(user.chat_id)
            )

        elif user.is_admin and user.is_owner:

            update.effective_message.bot.set_my_commands(
                get_owner_commands(language, user.language) + get_common_commands(language),
                scope=BotCommandScopeChat(user.chat_id)
            )
        

    update.message.reply_text('تم تحديث اوامر البوت لكل المستخدمين')

    return CHOICE