from flaskr.models import User
from flaskr.bot.owner.owner_constants import ANNOUNCEMENT_OPTIONS, RECIEVE_ANNOUNCEMENT
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update, ReplyKeyboardRemove
from flaskr.bot.utils.is_owner import is_owner
from flaskr import db




def view_announcement(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_owner(update, context, session):
        return

    announcement_text = context.chat_data['announcement_text']

    update.message.reply_text(announcement_text)

    return ANNOUNCEMENT_OPTIONS


def send_announcement(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_owner(update, context, session):
        return

    announcement_text = context.chat_data['announcement_text']

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

        if str(user.chat_id) == str(owner_chat_id):
            continue

        is_last = index == len(users) - 1

        when = index * 2

        context.job_queue.run_once(
            send_announcement_job,
            when,
            context=(
                announcement_text,
                user.chat_id,
                owner_chat_id,
                is_last,
            ),
            name=JOB_NAME
        )


def send_announcement_job(context):
    announcement_text = context.job.context[0]
    user_chat_id = context.job.context[1]
    owner_chat_id = context.job.context[2]
    is_last_user =  context.job.context[3]

    context.bot.send_message(user_chat_id, text=announcement_text)

    if is_last_user:
        context.bot.send_message(
            owner_chat_id,
            text=f'تم اعلان كافة المستخدمين'
        )


