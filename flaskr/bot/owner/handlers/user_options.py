from flaskr.bot.owner.handlers.update_commands import set_commands_job
from flaskr.bot.owner.handlers.view_user import view_user
from flaskr.bot.utils.is_owner import is_owner
from flaskr.bot.owner.handlers.choice import  list_users
from flaskr import db
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update
from flaskr.bot.utils.user_required import user_required
from flaskr.models import ChatData, User, UserData



def delete_user(update: Update, context: CallbackContext) -> int:

    session = db.session
    
    if not is_owner(update, context, session):
        return

    # read from context
    user_id = context.chat_data['viewed_user_id']

    user = session.query(User).filter(User.id==user_id).one_or_none()
    user_data = session.query(UserData).filter(UserData.user_id==user.telegram_id).one_or_none()
    chat_data = session.query(ChatData).filter(ChatData.chat_id==user.chat_id).one_or_none()

    if user:
        session.delete(user)
        session.delete(user_data)
        session.delete(chat_data)
        update.message.reply_text(f'تم حذف المستخدم {user.first_name} {user.last_name if user.last_name else ""}')
    else:
        update.message.reply_text(f'حدث خطا: لم يتم العثور على {user.first_name}')



    session.commit()
    session.close()
    return list_users(update, context)

def subscribe_user(update: Update, context: CallbackContext) -> int:

    session = db.session
    
    if not is_owner(update, context, session):
        return

    # read from context
    user_id = context.chat_data['viewed_user_id']

    user = session.query(User).filter(User.id==user_id).one()

    if user.chat_id:
        user.subscribed = True

        session.commit()

        update.message.reply_text(f'{user.first_name} {user.last_name if user.last_name else ""} اصبح مشتركاً الآن.')
    
    else:
        update.message.reply_text(
            f'{user.first_name} {user.last_name if user.last_name else ""} لا يمكنه الاشتراك.\n'
            f'error: chat_id is empty.')


    session.close()
    return view_user(update, context, user_id=user_id)

def unsubscribe_user(update: Update, context: CallbackContext) -> int:

    session = db.session
    
    if not is_owner(update, context, session):
        return

    # read from context
    user_id = context.chat_data['viewed_user_id']

    user = session.query(User).filter(User.id==user_id).one()

    user.subscribed = False

    session.commit()

    update.message.reply_text(f'{user.first_name} {user.last_name if user.last_name else ""} لم يعد مشتركاً.')

    session.close()
    return view_user(update, context, user_id=user_id)

def update_user_commands(update: Update, context: CallbackContext) -> int:

    session = db.session
    
    if not is_owner(update, context, session):
        return

    # read from context
    user_id = context.chat_data['viewed_user_id']

    user = session.query(User).filter(User.id==user_id).one()

    owner_chat_id = str(update.effective_chat.id)

    JOB_NAME = 'UPDATING_ACOMMANDS_FOR_USER' + str(user.chat_id)

    current_jobs = context.job_queue.get_jobs_by_name(JOB_NAME)

    for job in current_jobs:
        job.schedule_removal()

    context.job_queue.start()

    when = 0

    context.job_queue.run_once(
        set_commands_job,
        when,
        context=(user, owner_chat_id, True),
        name=JOB_NAME
        )

    session.close()
    return view_user(update, context, user_id=user_id)


