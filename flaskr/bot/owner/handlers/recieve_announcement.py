from flaskr.bot.owner.owner_constants import ANNOUNCEMENT_OPTIONS, RECIEVE_ANNOUNCEMENT
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from flaskr.bot.utils.is_owner import is_owner
from flaskr import db



def recieve_announcement(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_owner(update, context, session):
        return

    message = update.message.text

    if len(message) < 10:
        update.message.reply_text(
            'الرسالة قصيرة جدا. حاول مجدداً'
        )

        return RECIEVE_ANNOUNCEMENT

    # write to context
    context.chat_data['announcement_text'] = message


    reply_keyboard = []

    reply_keyboard.append(['عرض الاعلان', 'ارسال الاعلان'])

    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

    update.message.reply_text(
        'حسناً. الان لرؤية كيف سيبدو الاعلان اختر "عرض الاعلان" وستراه انت وحدك. اختر "ارسال الاعلان" عندما تكون مستعدا وسيتم ارساله لجميع المستخدمين.',
        reply_markup=markup
    )

    return ANNOUNCEMENT_OPTIONS