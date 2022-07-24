from flaskr.bot.utils.register_new_user import register_new_user
from flaskr.models import   User
from telegram.ext import  CallbackContext
from telegram import Update


def user_required(update: Update, context: CallbackContext, session) -> int:

    from_user = None

    if update.callback_query:
        from_user = update.callback_query.from_user

    if update.message:
        from_user = update.message.from_user

    user = None

    if not 'user_id' in context.user_data:
        user = register_new_user(
            session,
            first_name=from_user.first_name,
            last_name=from_user.last_name,
            telegram_id=from_user.id,
            chat_id=update.effective_chat.id,
            update=update,
            context=context,
        )
    
    elif 'user_id' in context.user_data:
        user = session.query(User).filter(User.telegram_id==from_user.id).one_or_none()
        
        if not user:
            user = register_new_user(
                session,
                first_name=from_user.first_name,
                last_name=from_user.last_name,
                telegram_id=from_user.id,
                chat_id=update.effective_chat.id,
                update=update,
                context=context,
            )

    if not user.chat_id:
        user.chat_id = update.effective_chat.id

        session.commit()

    return user