from flaskr.bot.owner.owner_constants import ANNOUNCEMENT_OPTIONS, RECIEVE_ANNOUNCEMENT
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from flaskr.bot.utils.is_owner import is_owner
from flaskr import db



def recieve_announcement(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_owner(update, context, session):
        return

    # write to context
    context.chat_data['announcement_message_id'] = update.effective_message.message_id

    reply_keyboard = []

    reply_keyboard.append(['عرض الاعلان', 'ارسال الاعلان'])
    reply_keyboard.append(['عرض الاعلان معلقا', 'ارسال الاعلان معلقا'])

    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

    update.message.reply_text(
        'حسناً. الان لرؤية كيف سيبدو الاعلان اختر "عرض الاعلان" وستراه انت وحدك. اختر "ارسال الاعلان" عندما تكون مستعدا وسيتم ارساله لجميع المستخدمين.',
        reply_markup=markup
    )

    return ANNOUNCEMENT_OPTIONS