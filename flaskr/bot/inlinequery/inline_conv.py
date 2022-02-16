from telegram.ext import InlineQueryHandler, ConversationHandler, CommandHandler, Filters, CallbackQueryHandler, MessageHandler
from flaskr.bot.inlinequery import handlers, inlinequery
from flaskr.bot.inlinequery.handlers import send_lab, send_lecture, send_references
from flaskr.bot.utils.cancel_conversation import cancel_conversation
import flaskr.bot.inlinequery.constants as constants



inline_conv = ConversationHandler(
    entry_points=[
      InlineQueryHandler(inlinequery),
      CommandHandler('start', send_lecture, Filters.regex(f'{constants.LECTURE}-\d+')),
      CommandHandler('start', send_lab, Filters.regex(f'{constants.LAB}-\d+')),
      CommandHandler('start', send_references, Filters.regex(f'{constants.REFERENCES}-\d+')),
    ],
    states={
      constants.SEND: [
      ]
    },
    fallbacks=[MessageHandler(Filters.command, cancel_conversation)],
    persistent=True,
    name="inline_conv",
    allow_reentry=True,
    per_chat=False,
)
