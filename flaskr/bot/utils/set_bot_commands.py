from telegram.botcommandscope import  BotCommandScopeChat
from telegram import Update
from telegram.ext import CallbackContext

def get_settings_commands(language):
    return [
        ('setlanguage',f"{language['language_settings']}".capitalize()),
    ]

def get_user_commands(language):
    return [
        ('courses', f"{language['courses']}".capitalize()),
    ]

def get_admin_commands(language):
    return get_user_commands(language) + [
        ('admin',f"{language['admin']}".capitalize()),
    ]

def get_owner_commands(language):
    return get_admin_commands(language) + [
        ('owner',f"{language['owner']}".capitalize()),
    ]
    


def set_bot_commands(update: Update, context: CallbackContext, user):

    language = context.chat_data['language']

    if not user.is_admin and not user.is_owner:

        update.effective_chat.bot.set_my_commands(
            get_user_commands(language) + get_settings_commands(language),
            scope=BotCommandScopeChat(update.effective_message.chat_id)
        )

    elif user.is_admin and not user.is_owner:
        
        update.effective_message.bot.set_my_commands(
            get_admin_commands(language) + get_settings_commands(language),
            scope=BotCommandScopeChat(update.effective_message.chat_id)
        )

    elif user.is_admin and user.is_owner:

        update.effective_message.bot.set_my_commands(
            get_owner_commands(language) + get_settings_commands(language),
            scope=BotCommandScopeChat(update.effective_message.chat_id)
        )
