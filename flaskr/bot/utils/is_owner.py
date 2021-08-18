from flaskr.bot.utils.user_required import user_required
from telegram.ext import  CallbackContext
from telegram import Update, ReplyKeyboardRemove


def is_owner(update: Update, context: CallbackContext, session) -> int:

    user = user_required(update, context, session)

    if not user.is_owner:
        update.message.reply_text('عذرا، ليست لديك صلاحيات ال admin', reply_markup=ReplyKeyboardRemove())
        return False

    else: 
        return  True