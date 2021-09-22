from telegram.ext import CallbackContext, CallbackContext
from telegram.botcommandscope import  BotCommandScopeChat
from telegram import Update
from flaskr.bot.localization import ar, en
from flaskr.bot.utils.is_owner import is_owner
from flaskr.bot.utils.set_bot_commands import get_admin_commands, get_common_commands, get_owner_commands, get_user_commands
from flaskr import db
from flaskr.models import User




def set_bot_commands(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_owner(update, context, session):
        return

    owner_chat_id = str(update.effective_chat.id)

    update.message.bot.send_message(
        owner_chat_id,
        text='جاري تحديث اوامر البوت. قد ياخذ هذا الامر بعض الوقت'
    )

    JOB_NAME = 'UPDATING_COMMANDS_' + owner_chat_id

    current_jobs = context.job_queue.get_jobs_by_name(JOB_NAME)

    for job in current_jobs:
        job.schedule_removal()

    users = session.query(User).all()

    context.job_queue.start()
    
    for (index, user) in enumerate(users):

        if not user.chat_id:
            continue

        is_last = index == len(users) - 1

        when = index * 10

        context.job_queue.run_once(
            set_commands_job,
            when,
            context=(user, owner_chat_id, is_last),
            name=JOB_NAME
        )


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

    if is_last_user:
        context.bot.send_message(
            owner_chat_id,
            text=f'تم تحديث اوامر البوت لكل المستخدمين'
        )


