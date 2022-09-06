import json
import re
from flaskr.bot.admin.handlers.labs.lab import publish
from flaskr.bot.notifications.notifications_constants import NOTIFIED_LAB 
from flaskr.bot.utils.is_admin import is_admin
from flaskr.bot.utils.get_user_language import get_user_language
from flaskr import db
from flaskr.models import  Lab, Lecture, User, UserSetting
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update, constants, InlineKeyboardButton, InlineKeyboardMarkup
from flaskr.user_settings import KEYS

course_regex = re.compile(r'\+c\+')
number_regex = re.compile(r'\+n\+')

def publish_silently(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    # read from to context
    lab_id = context.chat_data['lab_id']
    lab = session.query(Lab).filter(Lab.id==int(lab_id)).one()

    if lab.published:
        update.message.reply_text(
            'هذه اللاب نشر من قبل',
        )
        return publish(update, context)

    lab.published = True
    session.commit()

    update.message.reply_text(
        'تم النشر',
    )

    session.close()
    return publish(update, context)


def publish_with_notification(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    # read from to context
    lab_id = context.chat_data['lab_id']
    lab = session.query(Lab).filter(Lab.id==int(lab_id)).one()
    course = lab.course
    owner_chat_id = str(update.effective_chat.id)

    if lab.published:
        update.message.reply_text(
            'هذا اللاب نشر من قبل',
        )
        return publish(update, context)

    update.message.reply_text(
        'جاري ارسال التنبيه للمستخدمين. قد ياخذ هذا الامر بعض الوقت',
    )

    JOB_NAME = 'SENDING_LAB_NOTIFICATION_' + owner_chat_id

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

        course_name = course.ar_name \
            if user.language == 'ar' \
            else course.en_name

        context.job_queue.run_once(
            send__lecture_notification_job,
            when,
            context=(
                user.id,
                user.chat_id,
                user.language,
                owner_chat_id,
                is_last,
                lab.lab_number,
                lab.id,
                course_name,
            ),
            name=JOB_NAME
        )

    lab.published = True
    
    session.commit()

    return publish(update, context)

def send__lecture_notification_job(context: CallbackContext):
    user_id = context.job.context[0]
    chat_id = context.job.context[1]
    user_language = context.job.context[2]
    owner_chat_id = context.job.context[3]
    is_last_user =  context.job.context[4]
    lab_number =  context.job.context[5]
    lab_id =  context.job.context[6]
    course_name = context.job.context[7]

    session = db.session

    notify_on_lab = session.query(UserSetting) \
        .filter(UserSetting.user_id==user_id, UserSetting.key==KEYS['NOTIFY_ON_LAB']) \
        .one_or_none()
    notify_on_lab = json.loads(notify_on_lab.value) if notify_on_lab else True
    
    if not notify_on_lab:
        return

    language = get_user_language(user_language)

    keyboard = [
      [
            InlineKeyboardButton(f"{language['show'].capitalize()} {language['more']}",
            callback_data=f'{NOTIFIED_LAB} {lab_id}'),
      ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    template = language['notify_lab_template']
    message = re.sub(course_regex, course_name, template)
    message = '🔔  ' + re.sub(number_regex, f'{lab_number}', message)

    context.bot.send_message(
        text=message,
        reply_markup=reply_markup,
        chat_id=chat_id,
        parse_mode=constants.PARSEMODE_MARKDOWN_V2
    )


    if is_last_user:
        context.bot.send_message(
            owner_chat_id,
            text=f'تم اعلان كافة المستخدمين'
        )