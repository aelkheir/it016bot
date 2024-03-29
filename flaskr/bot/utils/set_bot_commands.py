from flaskr.bot.utils.get_user_language import get_user_language
from flaskr.models import Course
from telegram.botcommandscope import  BotCommandScopeChat
from telegram import Update
from telegram.ext import CallbackContext
from flaskr import db

def get_common_commands(language):
    return [
        ('setlanguage',f"{language['language_settings']}".capitalize()),
        # ('subscription',f"{language['subscription_settings']}".capitalize()),
        ('notifications',f"{language['notifications_settings']}".capitalize()),
    ]

def get_user_commands(language, user_language):

    return  [
        ("courses", f"{language['courses']}".capitalize()),
        ('archive', f"{language['archive']}".capitalize()),
    ] + get_common_commands(language)

def get_admin_commands(language, user_language):
    return get_user_commands(language, user_language) + [
        ('editcourses', f"{language['edit_courses']}".capitalize()),
    ]

def get_owner_commands(language, user_language):
    return get_admin_commands(language, user_language) + [
        ('editarchive', f"{language['edit_archive']}".capitalize()),
        ('manageusers', f"{language['manage_users']}".capitalize()),
        ('updatecommands', f"{language['update_commands']}".capitalize()),
        ('sendannouncement', f"{language['send_announcement']}".capitalize()),
    ]
    


def set_bot_commands(update: Update, context: CallbackContext, user):

    language = get_user_language(context.chat_data['language'])

    if not user.is_admin and not user.is_owner:

        update.effective_chat.bot.set_my_commands(
            get_user_commands(language, user.language),
            scope=BotCommandScopeChat(update.effective_message.chat_id)
        )

    elif user.is_admin and not user.is_owner:
        
        update.effective_message.bot.set_my_commands(
            get_admin_commands(language, user.language),
            scope=BotCommandScopeChat(update.effective_message.chat_id)
        )

    elif user.is_admin and user.is_owner:

        update.effective_message.bot.set_my_commands(
            get_owner_commands(language, user.language),
            scope=BotCommandScopeChat(update.effective_message.chat_id)
        )

