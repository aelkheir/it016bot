from flaskr.bot.utils.is_owner import is_owner
from flaskr.bot.owner.owner_constants import ADMIN_OPTIONS, RECIEVE_NEW_ADMIN
import re
from flaskr import db
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from flaskr.models import User



def view_admin(update: Update, context: CallbackContext) -> int:

    session = db.session

    if not is_owner(update, context, session):
        return

    id_regex = re.compile('(\d+)\s.*')
    match = id_regex.search(update.message.text)

    user_id = match.groups()[0]

    # write to context 
    context.chat_data['viewed_user_id'] = user_id

    user = session.query(User).filter(User.id==user_id).one()

    reply_keyboard = []
    reply_keyboard.append(['حذف من المدراء'])
    reply_keyboard.append(['رجوع'])

    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

    update.message.reply_text(
        f'{user.first_name} {user.last_name if user.last_name else ""}',
        reply_markup=markup,
    )

    return ADMIN_OPTIONS


def add_admin(update: Update, context: CallbackContext) -> int:

    session = db.session

    if not is_owner(update, context, session):
        return

    update.message.reply_text('ارسل رسالة (فورورد) من المدير الجديد', reply_markup=ReplyKeyboardRemove())

    session.close()
    return RECIEVE_NEW_ADMIN