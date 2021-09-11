from flaskr.bot.utils.is_owner import is_owner
import re
from flaskr.bot.owner.owner_constants import  USER_OPTIONS
from flaskr import db
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from flaskr.models import User



def view_user(update: Update, context: CallbackContext, user_id=None) -> int:

    session = db.session
    
    if not is_owner(update, context, session):
        return

    if not user_id:
        id_regex = re.compile('(\d+)\s.*')
        match = id_regex.search(update.message.text)

        user_id = match.groups()[0]

    # write to context 
    context.chat_data['viewed_user_id'] = user_id

    user = session.query(User).filter(User.id==user_id).one()

    reply_keyboard = []

    reply_keyboard.append(['اشتراك', 'الغاء الاشتراك'])

    reply_keyboard.append(['حذف المستخدم'])

    reply_keyboard.append(['رجوع'])

    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

    update.message.reply_text(
        f'{user.first_name} {user.last_name if user.last_name else ""}\n\n'
        f'start count: {user.start_count}\n'
        f'download count: {user.download_count}\n'
        f"subscription: {'subscribed' if user.subscribed else 'not subscribed'}",
        reply_markup=markup,
    )

    return USER_OPTIONS
