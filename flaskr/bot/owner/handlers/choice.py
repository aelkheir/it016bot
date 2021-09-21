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

    owner_chat_id = str(update.effective_chat.id)

    update.message.bot.send_message(
        owner_chat_id,
        text='جاري تحديث اوامر البوت. قد ياخذ هذا بعض الوقت'
    )


    current_jobs = context.job_queue.get_jobs_by_name(owner_chat_id)

    for job in current_jobs:
        job.schedule_removal()

    users = session.query(User).all()
    
    for (index, user) in enumerate(users):

        if not user.chat_id:
            continue

        is_last = index == len(users) - 1

        when = index * 20

        context.job_queue.run_once(
            set_commands_job,
            when,
            context=(user, owner_chat_id, is_last),
            name=owner_chat_id
        )

    return CHOICE

def set_commands_job(context):
    user = context.job.context[0]
    owner_chat_id = context.job.context[1]
    is_last_user =  context.job.context[2]

    language = ar\
    if user.language == 'ar'\
    else en

    if not user.is_admin and not user.is_owner:
        context.bot.set_my_commands(
            get_user_commands(language, user.language) + get_common_commands(language),
            scope=BotCommandScopeChat(user.chat_id)
        )

    elif user.is_admin and not user.is_owner:
        context.bot.set_my_commands(
            get_admin_commands(language, user.language) + get_common_commands(language),
            scope=BotCommandScopeChat(user.chat_id)
        )

    elif user.is_admin and user.is_owner:
        context.bot.set_my_commands(
            get_owner_commands(language, user.language) + get_common_commands(language),
            scope=BotCommandScopeChat(user.chat_id)
        )

    context.bot.send_message(
        owner_chat_id,
        text=f'تم تحديث اوامر البوت ل {user.first_name}'
    )
    
    if is_last_user:
        context.bot.send_message(
            owner_chat_id,
            text=f'تم تحديث اوامر البوت لكل المستخدمين'
        )

