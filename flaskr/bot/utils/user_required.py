from telegram.constants import BOT_COMMAND_SCOPE_ALL_PRIVATE_CHATS, BOT_COMMAND_SCOPE_CHAT
from flaskr.bot.utils.set_bot_commands import set_bot_commands
from telegram.botcommandscope import  BotCommandScope, BotCommandScopeAllPrivateChats, BotCommandScopeChat
from flaskr.bot.utils.register_new_user import register_new_user
from flaskr.models import   User
from flaskr import db
from telegram.ext import  CallbackContext
from telegram import Update
from flaskr.bot.localization.ar import ar
from flaskr.bot.localization.en import en


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
            chat_id=update.effective_chat.id
        )
        # write to context
        context.user_data['user_id'] = user.id
    
    elif 'user_id' in context.user_data:
        user = session.query(User).filter(User.telegram_id==from_user.id).one_or_none()
        
        if not user:
            user = register_new_user(
                session,
                first_name=from_user.first_name,
                last_name=from_user.last_name,
                telegram_id=from_user.id,
                chat_id=update.effective_chat.id
            )
            # write to context
            context.user_data['user_id'] = user.id

    if not user.chat_id:
        user.chat_id = update.effective_chat.id

        session.commit()

    if not 'language' in context.chat_data:
        # write to context
        context.chat_data['language'] = user.language

    # set_bot_commands(update, context, user)


    return user