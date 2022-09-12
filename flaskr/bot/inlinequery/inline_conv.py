from telegram.ext import InlineQueryHandler, ConversationHandler, CommandHandler, Filters, CallbackQueryHandler, MessageHandler
from flaskr.bot.inlinequery import handlers, inlinequery
from flaskr.bot.inlinequery.handlers import inline_help_message, send_assignment, send_exam, send_lab, send_lecture, send_references, send_tutorial
from flaskr.bot.user.user_constants import ASSIGNMENT, EXAM, LAB, LECTURE, REFFERENCES, TUTORIAL
from flaskr.bot.utils.cancel_conversation import cancel_conversation
import flaskr.bot.inlinequery.constants as constants



inline_conv = ConversationHandler(
    entry_points=[
      InlineQueryHandler(inlinequery),
      CommandHandler('start', inline_help_message, Filters.regex(f'{constants.INLINE_HELP}')),
      CommandHandler('start', send_lecture, Filters.regex(f'{LECTURE}-\d+')),
      CommandHandler('start', send_lab, Filters.regex(f'{LAB}-\d+')),
      CommandHandler('start', send_tutorial, Filters.regex(f'{TUTORIAL}-\d+')),
      CommandHandler('start', send_references, Filters.regex(f'{REFFERENCES}-\d+')),
      CommandHandler('start', send_assignment, Filters.regex(f'{ASSIGNMENT}-\d+')),
      CommandHandler('start', send_exam, Filters.regex(f'{EXAM}-\d+')),
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
