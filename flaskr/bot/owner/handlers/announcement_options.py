from flaskr.models import User
from flaskr.bot.owner.owner_constants import ANNOUNCEMENT_OPTIONS, RECIEVE_ANNOUNCEMENT
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update, ReplyKeyboardRemove
from flaskr.bot.utils.is_owner import is_owner
from flaskr import db




def view_announcement(update: Update, context: CallbackContext, pin=False) -> int:
    session = db.session

    if not is_owner(update, context, session):
        return

    message_id = context.chat_data['announcement_message_id']

    message = context.bot.copy_message(update.effective_message.chat_id, update.effective_message.chat_id, message_id)

    print('\n', message_id, '\n', pin)

    if pin == True:
        context.bot.pin_chat_message(update.effective_message.chat_id, message.message_id)

    return ANNOUNCEMENT_OPTIONS


def send_announcement(update: Update, context: CallbackContext, pin=False) -> int:
    session = db.session

    if not is_owner(update, context, session):
        return

    message_id = context.chat_data['announcement_message_id']

    owner_chat_id = str(update.effective_chat.id)

    update.message.reply_text(
        'جاري ارسال الاعلان لكل المستخدمين. قد ياخذ هذا الامر بعض الوقت',
        reply_markup=ReplyKeyboardRemove()
    )

    JOB_NAME = 'SENDING_ANNOUNCEMENT_' + owner_chat_id

    current_jobs = context.job_queue.get_jobs_by_name(JOB_NAME)

    for job in current_jobs:
        job.schedule_removal()

    users = session.query(User).all()

    context.job_queue.start()

    for (index, user) in enumerate(users):

        if not user.chat_id:
            continue

        is_last = index == len(users) - 1

        when = index * 2

        context.job_queue.run_once(
            send_announcement_job,
            when,
            context=(
                message_id,
                user.chat_id,
                owner_chat_id,
                is_last,
                user.subscribed,
                pin
            ),
            name=JOB_NAME
        )


def send_announcement_job(context):
    message_id = context.job.context[0]
    user_chat_id = context.job.context[1]
    owner_chat_id = context.job.context[2]
    is_last_user =  context.job.context[3]
    subscribed = context.job.context[4]
    pin = context.job.context[5]
    
    if subscribed:
        message = context.bot.copy_message(user_chat_id, owner_chat_id, message_id)
        if pin == True:
            context.bot.pin_chat_message(user_chat_id, message.message_id)

    if is_last_user:
        context.bot.send_message(
            owner_chat_id,
            text=f'تم اعلان كافة المستخدمين'
        )



