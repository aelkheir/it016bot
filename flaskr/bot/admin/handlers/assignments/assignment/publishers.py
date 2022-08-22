import json
import re
from flaskr.bot.admin.admin_constants import LECTURE_FILE_OPTIONS, PUBLISH_LECTURE
from flaskr.bot.admin.handlers.assignments.assignment import publish
from flaskr.bot.notifications.notifications_constants import SEND_NOTIFIED_ASSIGNMENT
from flaskr.bot.utils.is_admin import is_admin
from flaskr.bot.utils.get_user_language import get_user_language
from flaskr import db
from flaskr.models import  Assignment, Lecture, User, UserSetting
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
    assignment_id = context.chat_data['assignment_id']
    assignment = session.query(Assignment).filter(Assignment.id==int(assignment_id)).one()

    if assignment.published:
        update.message.reply_text(
            'هذا التسليم نشر من قبل',
        )
        return publish(update, context)

    assignment.published = True
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
    assignment_id = context.chat_data['assignment_id']
    assignment = session.query(Assignment).filter(Assignment.id==int(assignment_id)).one()
    course = assignment.course
    owner_chat_id = str(update.effective_chat.id)

    if assignment.published:
        update.message.reply_text(
            'هذا التسليم نشر من قبل',
        )
        return publish(update, context)

    update.message.reply_text(
        'جاري ارسال التنبيه للمستخدمين. قد ياخذ هذا الامر بعض الوقت',
    )

    JOB_NAME = 'SENDING_ASSIGNMENT_NOTIFICATION_' + owner_chat_id

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
                assignment.assignment_number,
                assignment.id,
                course_name,
            ),
            name=JOB_NAME
        )

    assignment.published = True
    
    session.commit()

    return publish(update, context)

def send__lecture_notification_job(context: CallbackContext):
    user_id = context.job.context[0]
    chat_id = context.job.context[1]
    user_language = context.job.context[2]
    owner_chat_id = context.job.context[3]
    is_last_user =  context.job.context[4]
    assignment_number =  context.job.context[5]
    assignment_id =  context.job.context[6]
    course_name = context.job.context[7]

    session = db.session

    notify_on_assignment = session.query(UserSetting) \
        .filter((UserSetting.user_id==user_id) & (UserSetting.key==KEYS['NOTIFY_ON_ASSIGNMENT'])) \
        .one_or_none()
    notify_on_assignment = json.loads(notify_on_assignment.value) if notify_on_assignment else True
    
    if not notify_on_assignment:
        return

    language = get_user_language(user_language)

    keyboard = [
      [
            InlineKeyboardButton(f"{language['assignment'].capitalize()} {assignment_number}",
            callback_data=f'{SEND_NOTIFIED_ASSIGNMENT} {assignment_id}'),
      ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    template = language['notify_assignment_template']
    message = re.sub(course_regex, course_name, template)
    message = '🔔  ' + re.sub(number_regex, f'{assignment_number}', message)

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