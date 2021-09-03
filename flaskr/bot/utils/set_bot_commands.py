from flaskr.models import Course
from telegram.botcommandscope import  BotCommandScopeChat
from telegram import Update
from telegram.ext import CallbackContext
from flaskr import db

def get_settings_commands(language):
    return [
        ('setlanguage',f"{language['language_settings']}".capitalize()),
    ]

def get_user_commands(language, user_language):
    session = db.session()

    courses = session.query(Course)\
        .filter(Course.en_course_symbol!='')\
        .order_by(Course.id).all()

    courses_commands = []

    for course in courses:

        course_name = course.ar_name \
            if user_language == 'ar' \
            else course.en_name
        course_name = course_name if course_name else course.ar_name

        courses_commands.append((f'{course.en_course_symbol}', f'{course_name}'.capitalize()))

    session.close()

    return [
        ('courses', f"{language['courses']}".capitalize()),
    ] + courses_commands

def get_admin_commands(language, user_language):
    return get_user_commands(language, user_language) + [
        ('admin',f"{language['admin']}".capitalize()),
    ]

def get_owner_commands(language, user_language):
    return get_admin_commands(language, user_language) + [
        ('owner',f"{language['owner']}".capitalize()),
    ]
    


def set_bot_commands(update: Update, context: CallbackContext, user):

    language = context.chat_data['language']

    if not user.is_admin and not user.is_owner:

        update.effective_chat.bot.set_my_commands(
            get_user_commands(language, user.language) + get_settings_commands(language),
            scope=BotCommandScopeChat(update.effective_message.chat_id)
        )

    elif user.is_admin and not user.is_owner:
        
        update.effective_message.bot.set_my_commands(
            get_admin_commands(language, user.language) + get_settings_commands(language),
            scope=BotCommandScopeChat(update.effective_message.chat_id)
        )

    elif user.is_admin and user.is_owner:

        update.effective_message.bot.set_my_commands(
            get_owner_commands(language, user.language) + get_settings_commands(language),
            scope=BotCommandScopeChat(update.effective_message.chat_id)
        )

