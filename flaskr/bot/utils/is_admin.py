from flaskr.bot.utils.user_required import user_required
from telegram.ext import  CallbackContext
from telegram import Update, ReplyKeyboardRemove


def is_admin(update: Update, context: CallbackContext, session) -> int:

    user = user_required(update, context, session)

    if not user.is_admin:
        update.message.reply_text('لا :(', reply_markup=ReplyKeyboardRemove())
        return False

    else: 
        return  True