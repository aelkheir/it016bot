from flaskr.models import User
from flaskr.bot.utils.set_bot_commands import set_bot_commands
from telegram.ext.filters import Filters
from flaskr.bot.utils.user_required import user_required
from flaskr.bot.utils.get_user_language import get_user_language
from flaskr.bot.utils.cancel_conversation import cancel_conversation
from telegram.ext import CommandHandler, CallbackContext, ConversationHandler, MessageHandler
from telegram import Update, ReplyKeyboardRemove
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from flaskr import db

from flaskr.bot.localization.ar import ar
from flaskr.bot.localization.en import en


RECIEVE_CHOICE = 0


def subscription_handler(update: Update, context: CallbackContext):
    session = db.session

    user = user_required(update, context, session)
    language = get_user_language(context.chat_data['language'])

    reply_keyboard = [
        [language['subscribe'].capitalize(), language['unsubscribe'].capitalize()]
    ]

    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

    current_status = language['subscribed'] if user.subscribed else language['unsubscribed']

    update.message.reply_text(
        f"{language['current_status']}: ".capitalize() + current_status.capitalize(),
        reply_markup=markup,
    )

    return RECIEVE_CHOICE

def recieve_subscription_choice(update: Update, context: CallbackContext):
    session = db.session

    user = user_required(update, context, session)

    user = session.query(User).filter(User.id==user.id).one()

    language = get_user_language(context.chat_data['language'])

    subscription_choice = update.message.text

    success = False

    if subscription_choice == language['subscribe'].capitalize():
        user.subscribed = True
        success = True

    elif subscription_choice == language['unsubscribe'].capitalize():
        user.subscribed = False
        success = True
    

    if success:

        session.commit()

        feedback_message = language['subscribed_successfully'] \
            if user.subscribed \
            else language['unsubscribed_successfully']

        update.message.reply_text(
            feedback_message.capitalize(),
            reply_markup=ReplyKeyboardRemove(),
        )

    session.close()
        



subscription_conv = ConversationHandler(
    entry_points=[CommandHandler('subscription', subscription_handler)],
    states={
        RECIEVE_CHOICE: {
            MessageHandler(Filters.text & ~ Filters.command, recieve_subscription_choice)
        }
    },
    fallbacks=[],
    name="subscription_conv",
    allow_reentry=True
)