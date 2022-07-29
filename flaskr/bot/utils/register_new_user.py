import os
from flaskr.models import User
from flaskr.bot.utils.set_bot_commands import set_bot_commands


def register_new_user(session, first_name, last_name, telegram_id, chat_id, update, context):

    is_owner, is_admin = False, False

    if str(telegram_id) in os.getenv('OWNER_IDS'):
        is_owner, is_admin = True, True


    user = session.query(User).filter(User.telegram_id==telegram_id).one_or_none()

    if not user:
        user = User(
            first_name=first_name,
            last_name=last_name,
            telegram_id=telegram_id,
            chat_id=chat_id,
            is_admin=is_admin,
            is_owner=is_owner,
        )
        session.add(user)
        session.commit()

    if not 'language' in context.chat_data:
        # write to context
        context.chat_data['language'] = user.language

    if not 'user_id' in context.chat_data:
        # write to context
        context.user_data['user_id'] = user.id

    set_bot_commands(update, context, user)

    return user
