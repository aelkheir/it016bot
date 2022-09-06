import json
from flaskr.bot.notifications.handle_notifications import handle_notifications
from flaskr.bot.notifications.notifications_constants import RECEIVE_ENTRY_NOTIFICATIONS
from flaskr.bot.utils.buttons import back_to_notification_settings
from flaskr.models import User, UserSetting
from flaskr.bot.utils.user_required import user_required
from flaskr.bot.utils.get_user_language import get_user_language
from telegram.ext import  CallbackContext
from telegram import Update, constants, InlineKeyboardMarkup, InlineKeyboardButton
from flaskr import db
from ...user_settings import KEYS

def recieve_notify_on_lecture(update: Update, context: CallbackContext):
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)
    user = session.query(User).filter(User.id==user.id).one()

    language = get_user_language(context.chat_data['language'])

    _, notify_on_lecture = query.data.split(' ')
    notify_on_lecture = bool(int(notify_on_lecture))

    user_setting = session.query(UserSetting) \
      .filter(UserSetting.user_id==user.id, UserSetting.key==KEYS['NOTIFY_ON_LECTURE']) \
      .one_or_none()

    if user_setting is None:
      user_setting = UserSetting(
        key=KEYS['NOTIFY_ON_LECTURE'],
        value=json.dumps(notify_on_lecture)
      )
      user_setting.user = user
      session.add(user_setting)
    else:
      user_setting.value = json.dumps(notify_on_lecture)

    option = language['turn_off'] if notify_on_lecture else language['turn_on']

    keyboard = [
        [
            InlineKeyboardButton(
                f'{option.capitalize()}',
                callback_data=f'{KEYS["NOTIFY_ON_LECTURE"]} {int(not notify_on_lecture)}'
            ),
        ],
        [
            back_to_notification_settings(language, user.language)
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    message = f"{language['lecture_notification']} {language['are']} *{language['enabled'] + '  🧿' if notify_on_lecture else language['disabled'] + '  🔘'}*"

    query.edit_message_text(
        f"{message}".capitalize(),
        reply_markup=reply_markup,
        parse_mode=constants.PARSEMODE_MARKDOWN_V2,
    )

    session.commit()
    session.close()

    return RECEIVE_ENTRY_NOTIFICATIONS

def recieve_notify_on_lab(update: Update, context: CallbackContext):
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)
    user = session.query(User).filter(User.id==user.id).one()

    language = get_user_language(context.chat_data['language'])

    _, notify_on_lab = query.data.split(' ')
    notify_on_lab = bool(int(notify_on_lab))

    user_setting = session.query(UserSetting) \
      .filter(UserSetting.user_id==user.id, UserSetting.key==KEYS['NOTIFY_ON_LAB']) \
      .one_or_none()

    if user_setting is None:
      user_setting = UserSetting(
        key=KEYS['NOTIFY_ON_LAB'],
        value=json.dumps(notify_on_lab)
      )
      user_setting.user = user
      session.add(user_setting)

    else:
      user_setting.value = json.dumps(notify_on_lab)

    option = language['turn_off'] if notify_on_lab else language['turn_on']

    keyboard = [
        [
            InlineKeyboardButton(
                f'{option.capitalize()}',
                callback_data=f'{KEYS["NOTIFY_ON_LAB"]} {int(not notify_on_lab)}'
            ),
        ],
        [
            back_to_notification_settings(language, user.language)
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    message = f"{language['lab_notification']} {language['are']} *{language['enabled'] + '  🧿' if notify_on_lab else language['disabled'] + '  🔘'}*"

    query.edit_message_text(
        f"{message}".capitalize(),
        reply_markup=reply_markup,
        parse_mode=constants.PARSEMODE_MARKDOWN_V2,
    )

    session.commit()
    session.close()

    return RECEIVE_ENTRY_NOTIFICATIONS

def recieve_notify_on_tutorial(update: Update, context: CallbackContext):
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)
    user = session.query(User).filter(User.id==user.id).one()

    language = get_user_language(context.chat_data['language'])

    _, notify_on_tutorial = query.data.split(' ')
    notify_on_tutorial = bool(int(notify_on_tutorial))

    user_setting = session.query(UserSetting) \
      .filter(UserSetting.user_id==user.id, UserSetting.key==KEYS['NOTIFY_ON_TUTORIAL']) \
      .one_or_none()

    if user_setting is None:
      user_setting = UserSetting(
        key=KEYS['NOTIFY_ON_TUTORIAL'],
        value=json.dumps(notify_on_tutorial)
      )
      user_setting.user = user
      session.add(user_setting)

    else:
      user_setting.value = json.dumps(notify_on_tutorial)

    option = language['turn_off'] if notify_on_tutorial else language['turn_on']

    keyboard = [
        [
            InlineKeyboardButton(
                f'{option.capitalize()}',
                callback_data=f'{KEYS["NOTIFY_ON_TUTORIAL"]} {int(not notify_on_tutorial)}'
            ),
        ],
        [
            back_to_notification_settings(language, user.language)
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    message = f"{language['tutorial_notification']} {language['are']} *{language['enabled'] + '  🧿' if notify_on_tutorial else language['disabled'] + '  🔘'}*"

    query.edit_message_text(
        f"{message}".capitalize(),
        reply_markup=reply_markup,
        parse_mode=constants.PARSEMODE_MARKDOWN_V2,
    )

    session.commit()
    session.close()

    return RECEIVE_ENTRY_NOTIFICATIONS

        
def recieve_notify_on_assignment(update: Update, context: CallbackContext):
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)
    user = session.query(User).filter(User.id==user.id).one()

    language = get_user_language(context.chat_data['language'])

    _, notify_on_assignment = query.data.split(' ')
    notify_on_assignment = bool(int(notify_on_assignment))

    user_setting = session.query(UserSetting) \
      .filter(UserSetting.user_id==user.id, UserSetting.key==KEYS['NOTIFY_ON_ASSIGNMENT']) \
      .one_or_none()

    if user_setting is None:
      user_setting = UserSetting(
        key=KEYS['NOTIFY_ON_ASSIGNMENT'],
        value=json.dumps(notify_on_assignment)
      )
      user_setting.user = user
      session.add(user_setting)

    else:
      user_setting.value = json.dumps(notify_on_assignment)

    session.commit()

    option = language['turn_off'] if notify_on_assignment else language['turn_on']

    keyboard = [
        [
            InlineKeyboardButton(
                f'{option.capitalize()}',
                callback_data=f'{KEYS["NOTIFY_ON_ASSIGNMENT"]} {int(not notify_on_assignment)}'
            ),
        ],
        [
            back_to_notification_settings(language, user.language)
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    message = f"{language['assignment_notification']} {language['are']} *{language['enabled'] + '  🧿' if notify_on_assignment else language['disabled'] + '  🔘'}*"

    query.edit_message_text(
        f"{message}".capitalize(),
        reply_markup=reply_markup,
        parse_mode=constants.PARSEMODE_MARKDOWN_V2,
    )

    session.close()

    return RECEIVE_ENTRY_NOTIFICATIONS