import json
from flaskr.bot.notifications.handle_notifications import handle_notifications
from flaskr.bot.notifications.notifications_constants import  RECEIVE_ENTRY_NOTIFICATIONS
from ..utils.buttons import back_to_notification_settings
from flaskr.bot.utils.get_user_language import get_user_language
from flaskr.bot.utils.user_required import user_required
from flaskr import db
from telegram.ext import CallbackContext
from telegram import  constants, Update, InlineKeyboardButton, InlineKeyboardMarkup
from flaskr.models import User, UserSetting
from ...user_settings import KEYS

def set_lecture_notification(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)
    language = get_user_language(context.chat_data['language'])

    user_setting = session.query(UserSetting) \
      .filter(UserSetting.user_id==user.id, UserSetting.key==KEYS['NOTIFY_ON_LECTURE']) \
      .one_or_none()

    current_setting = json.loads(user_setting.value) if user_setting else True

    option = language['turn_off'] if current_setting else language['turn_on']

    keyboard = [
        [
            InlineKeyboardButton(
                f'{option.capitalize()}',
                callback_data=f'{KEYS["NOTIFY_ON_LECTURE"]} {int(not current_setting)}'
            ),
        ],
        [
            back_to_notification_settings(language, user.language)
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    message = f"{language['lecture_notification']} {language['are']} *{language['enabled'] + '  🧿' if current_setting else language['disabled'] + '  🔘'}*"

    query.message.edit_text(
        f"{message}".capitalize(),
        reply_markup=reply_markup,
        parse_mode=constants.PARSEMODE_MARKDOWN_V2,
    )

    return RECEIVE_ENTRY_NOTIFICATIONS

def set_labs_notification(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)
    language = get_user_language(context.chat_data['language'])

    user_setting = session.query(UserSetting) \
      .filter(UserSetting.user_id==user.id, UserSetting.key==KEYS['NOTIFY_ON_LAB']) \
      .one_or_none()

    current_setting = json.loads(user_setting.value) if user_setting else True

    option = language['turn_off'] if current_setting else language['turn_on']

    keyboard = [
        [
            InlineKeyboardButton(
                f'{option.capitalize()}',
                callback_data=f'{KEYS["NOTIFY_ON_LAB"]} {int(not current_setting)}'
            ),
        ],
        [
            back_to_notification_settings(language, user.language)
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    message = f"{language['lab_notification']} {language['are']} *{language['enabled'] + '  🧿' if current_setting else language['disabled'] + '  🔘'}*"

    query.message.edit_text(
        f"{message}".capitalize(),
        reply_markup=reply_markup,
        parse_mode=constants.PARSEMODE_MARKDOWN_V2,
    )

    return RECEIVE_ENTRY_NOTIFICATIONS

def set_assignment_notification(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)
    language = get_user_language(context.chat_data['language'])

    user_setting = session.query(UserSetting) \
      .filter(UserSetting.user_id==user.id, UserSetting.key==KEYS['NOTIFY_ON_ASSIGNMENT']) \
      .one_or_none()

    current_setting = json.loads(user_setting.value) if user_setting else True

    option = language['turn_off'] if current_setting else language['turn_on']

    keyboard = [
        [
            InlineKeyboardButton(
                f'{option.capitalize()}',
                callback_data=f'{KEYS["NOTIFY_ON_ASSIGNMENT"]} {int(not current_setting)}'
            ),
        ],
        [
            back_to_notification_settings(language, user.language)
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    message = f"{language['assignment_notification']} {language['are']} *{language['enabled'] + '  🧿' if current_setting else language['disabled'] + '  🔘'}*"

    query.message.edit_text(
        f"{message}".capitalize(),
        reply_markup=reply_markup,
        parse_mode=constants.PARSEMODE_MARKDOWN_V2,
    )

    return RECEIVE_ENTRY_NOTIFICATIONS


def disable_all_notifications(update: Update, context: CallbackContext):
    session = db.session

    user = user_required(update, context, session)
    user = session.query(User).filter(User.id==user.id).one()

    language = get_user_language(context.chat_data['language'])

    has_changed = False

    notify_on_lecture = session.query(UserSetting) \
      .filter(UserSetting.user_id==user.id, UserSetting.key==KEYS['NOTIFY_ON_LECTURE']) \
      .one_or_none()
    if notify_on_lecture is not None and json.loads(notify_on_lecture.value):
      notify_on_lecture.value = json.dumps(False)
      has_changed = True
    elif notify_on_lecture is None:
      notify_on_lecture = UserSetting(
        key=KEYS['NOTIFY_ON_LECTURE'],
        value=json.dumps(False)
      )
      notify_on_lecture.user = user
      session.add(notify_on_lecture)

    notify_on_lab = session.query(UserSetting) \
      .filter(UserSetting.user_id==user.id, UserSetting.key==KEYS['NOTIFY_ON_LAB']) \
      .one_or_none()
    if notify_on_lab is not None and json.loads(notify_on_lab.value):
      notify_on_lab.value = json.dumps(False) 
      has_changed = True
    elif notify_on_lab is None:
      notify_on_lab = UserSetting(
        key=KEYS['NOTIFY_ON_LAB'],
        value=json.dumps(False)
      )
      notify_on_lab.user = user
      session.add(notify_on_lab)
    
    notify_on_assignment = session.query(UserSetting) \
      .filter(UserSetting.user_id==user.id, UserSetting.key==KEYS['NOTIFY_ON_ASSIGNMENT']) \
      .one_or_none()
    if notify_on_assignment is not None and json.loads(notify_on_assignment.value):
      notify_on_assignment.value = json.dumps(False)
      has_changed = True
    elif notify_on_assignment is None:
      notify_on_assignment = UserSetting(
        key=KEYS['NOTIFY_ON_ASSIGNMENT'],
        value=json.dumps(False)
      )
      notify_on_assignment.user = user

      session.add(notify_on_assignment)

    query = update.callback_query

    if has_changed:
      query.answer()
    else:
      query.answer(text=language['all_notifications_are_off'].capitalize(), show_alert=True)

    session.commit()
    session.close()

    return handle_notifications(update, context, has_changed)