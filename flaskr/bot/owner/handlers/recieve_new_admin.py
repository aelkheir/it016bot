from flaskr.bot.utils.is_owner import is_owner
from flaskr.bot.utils.register_new_user import register_new_user
import re
from flaskr import db
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update
from flaskr.models import User
from flaskr.bot.owner.handlers.choice import list_admins
from flaskr.bot.owner.owner_constants import ADMIN_OPTIONS, RECIEVE_NEW_ADMIN



def recieve_new_admin(update: Update, context: CallbackContext) -> int:

    session = db.session

    if not is_owner(update, context, session):
        return

    forward_from = update.message.forward_from

    user = session.query(User).filter(User.telegram_id==forward_from.id).one_or_none()

    if not user:
        user = register_new_user(session, forward_from.first_name, forward_from.last_name, forward_from.id)

    user.is_admin = True

    update.message.reply_text(f'اصبح {user.first_name} مديرا الان.')

    session.commit()
    session.close()
    return list_admins(update, context)
