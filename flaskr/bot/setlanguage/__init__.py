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


def language_handler(update: Update, context: CallbackContext):
    session = db.session

    user_required(update, context, session)
    language = get_user_language(context.chat_data['language'])

    reply_keyboard = [
        ['العربية', 'English']
    ]

    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

    update.message.reply_text(
        f"{language['select_bot_language']}".capitalize(),
        reply_markup=markup,
    )

    return RECIEVE_CHOICE

def recieve_language_choice(update: Update, context: CallbackContext):
    session = db.session

    user = user_required(update, context, session)

    user = session.query(User).filter(User.id==user.id).one()

    language_choice = update.message.text

    success = False

    if language_choice == 'العربية':
        user.language = 'ar'
        success = True

    elif language_choice == 'English':
        user.language = 'en'
        success = True
    

    if success:

        session.commit()

        # write to context
        context.chat_data['language'] = user.language

        language = get_user_language(context.chat_data['language'])

        update.message.reply_text(
            f"{language['language_set_to']}",
            reply_markup=ReplyKeyboardRemove(),
        )
        set_bot_commands(update, context, user)

    session.close()
        



language_conv = ConversationHandler(
    entry_points=[CommandHandler('setlanguage', language_handler)],
    states={
        RECIEVE_CHOICE: {
            MessageHandler(Filters.text & ~ Filters.command, recieve_language_choice)
        }
    },
    fallbacks=[],
    name="language_conv",
    allow_reentry=True
)