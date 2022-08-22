import json
import flaskr.bot.notifications.notifications_constants as myconstants
from flaskr.bot.utils.get_user_language import get_user_language
from flaskr.bot.utils.user_required import user_required
from flaskr.models import  User, UserSetting
from flaskr import db
from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, constants

from flaskr.user_settings import KEYS

on_icon = '🧿'
off_icon = '🔘'

def handle_notifications(update: Update, context: CallbackContext, has_changed=True) -> int:
    session = db.session

    query = update.callback_query
    if query:
        query.answer()

    user = user_required(update, context, session)
    language = get_user_language(context.chat_data['language'])

    user = session.query(User).filter(User.id==user.id).one()

    keyboard = [
        [
            InlineKeyboardButton(
                f'{language["disable_all"].title()}',
                callback_data=f'{myconstants.DISABLE_ALL}'
            ),
        ],
        [
            InlineKeyboardButton(
                f'{language["lecture_notification"].title()}',
                callback_data=f'{myconstants.LECTURE_NOTIFICATION}'
            )
        ],
        [
            InlineKeyboardButton(
                f'{language["lab_notification"].title()}',
                callback_data=f'{myconstants.LAB_NOTIFICATION}'
            ),
        ],
        [
            InlineKeyboardButton(
                f'{language["assignment_notification"].title()}',
                callback_data=f'{myconstants.ASSIGNMENT_NOTIFICATION}'
            ),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)


    lecture_setting = session.query(UserSetting) \
        .filter(UserSetting.user_id==user.id, UserSetting.key==KEYS['NOTIFY_ON_LECTURE']) \
        .one_or_none()
    lecture_setting = json.loads(lecture_setting.value) if lecture_setting else True
    notify_on_lecture = language["turned_on"].capitalize()  \
        if lecture_setting \
        else language["turned_off"].capitalize()

    lab_setting = session.query(UserSetting) \
        .filter(UserSetting.user_id==user.id, UserSetting.key==KEYS['NOTIFY_ON_LAB']) \
        .one_or_none()
    lab_setting = json.loads(lab_setting.value) if lab_setting else True
    notify_on_lab = language["turned_on"].capitalize()  \
        if lab_setting \
        else language["turned_off"].capitalize()

    assignment_setting = session.query(UserSetting) \
        .filter(UserSetting.user_id==user.id, UserSetting.key==KEYS['NOTIFY_ON_ASSIGNMENT']) \
        .one_or_none()
    assignment_setting = json.loads(assignment_setting.value) if assignment_setting else True
    notify_on_assignment = language["turned_on"].capitalize()  \
        if assignment_setting \
        else language["turned_off"].capitalize()

    lectures_notification = f"*{language['lecture_notification']}*:  ".title()
    lab_notification = f"*{language['lab_notification']}*:  ".title()
    assignment_notification = f"*{language['assignment_notification']}*:  ".title()

    lecture_icon = on_icon if lecture_setting else off_icon
    lab_icon = on_icon if lab_setting else off_icon
    assignment_icon = on_icon if assignment_setting else off_icon

    reply_text = '*%s*\n\n' %  language["notifications"].title() + \
                 '%s %s  %s\n' % (lectures_notification, notify_on_lecture, lecture_icon) + \
                 '%s %s  %s\n' % (lab_notification, notify_on_lab, lab_icon) + \
                 '%s %s  %s\n' % (assignment_notification, notify_on_assignment, assignment_icon) 

    if query and has_changed:
        query.edit_message_text(
            reply_text,
            reply_markup=reply_markup,
            parse_mode=constants.PARSEMODE_MARKDOWN_V2,
        )

    elif update.message:
        update.message.reply_text(
            reply_text,
            reply_markup=reply_markup,
            parse_mode=constants.PARSEMODE_MARKDOWN_V2
        )

    session.close()

    return myconstants.ENTRY_POINTS

