from telegram.ext import CallbackContext, CallbackContext, ConversationHandler
from telegram import Update


def cancel_conversation(update: Update, context: CallbackContext) -> int:
    return ConversationHandler.END