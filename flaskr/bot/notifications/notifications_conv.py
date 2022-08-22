from telegram.ext import  ConversationHandler, CallbackQueryHandler
from flaskr.bot.notifications.handle_notifications import handle_notifications
import flaskr.bot.notifications.notifications_constants as constants
from flaskr.bot.notifications.notified_lab_options import lab_notification_message
from flaskr.bot.user.handlers.stage_foure import send_all_lab_files
import flaskr.bot.user.user_constants as user_constants
from flaskr.bot.notifications.notified_entry import list_notified_lab_files, list_notified_lecture_files
from flaskr.bot.notifications.notified_lecture_options import lecture_notification_message
from flaskr.bot.notifications.set_entry_notifications import disable_all_notifications, set_lecture_notification, set_assignment_notification, set_labs_notification
import flaskr.bot.notifications.receivers as receivers
from flaskr.bot.user.handlers.stage_three import send_all_lecture_files, send_assignment, send_file
from ...user_settings import KEYS


notifications_conv = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            set_lecture_notification, pattern='^' + f'{constants.LECTURE_NOTIFICATION}' + '$'
        ),
        CallbackQueryHandler(
            set_labs_notification, pattern='^' + f'{constants.LAB_NOTIFICATION}' + '$'
        ),
        CallbackQueryHandler(
            set_assignment_notification, pattern='^' + f'{constants.ASSIGNMENT_NOTIFICATION}' + '$'
        ),
        CallbackQueryHandler(
            disable_all_notifications,
            pattern='^' + f'{constants.DISABLE_ALL}' + '$'
        ),
        CallbackQueryHandler(
            list_notified_lecture_files,
            pattern='^' + f'{constants.NOTIFIED_LECTURE}\s\d+' + '$'
        ),
        CallbackQueryHandler(
            list_notified_lab_files,
            pattern='^' + f'{constants.NOTIFIED_LAB}\s\d+' + '$'
        ),
        CallbackQueryHandler(
            send_assignment,
            pattern='^' + f'{constants.SEND_NOTIFIED_ASSIGNMENT}\s\d+' + '$'
        ),
    ],
    states={
        constants.RECEIVE_ENTRY_NOTIFICATIONS: [
            CallbackQueryHandler(
                receivers.recieve_notify_on_lecture,
                pattern='^' + f'{KEYS["NOTIFY_ON_LECTURE"]}\s\d' + '$'
            ),
            CallbackQueryHandler(
                receivers.recieve_notify_on_lab,
                pattern='^' + f'{KEYS["NOTIFY_ON_LAB"]}\s\d' + '$'
            ),
            CallbackQueryHandler(
                receivers.recieve_notify_on_assignment,
                pattern='^' + f'{KEYS["NOTIFY_ON_ASSIGNMENT"]}\s\d' + '$'
            ),
            CallbackQueryHandler(
                handle_notifications,
                pattern='^' + f'{constants.NOTIFICATIONS_SETTINGS}' + '$'
            ),
        ],
        constants.NOTIFIED_LECTURE_OPTIONS: [
            CallbackQueryHandler(
                lecture_notification_message,
                pattern='^' + f'{constants.LECTURE_NOTIFICATION_MESSAGE} \d+' + '$'
            ),
            CallbackQueryHandler(send_file, pattern='^' + f'{user_constants.FILE} .+' + '$'),
            CallbackQueryHandler(send_all_lecture_files, pattern='^' + f'{user_constants.LECTURE} \d+' + '$'),
        ],

        constants.NOTIFIED_LAB_OPTIONS: [
            CallbackQueryHandler(
                lab_notification_message,
                pattern='^' + f'{constants.LAB_NOTIFICATION_MESSAGE} \d+' + '$'
            ),
            CallbackQueryHandler(send_file, pattern='^' + f'{user_constants.FILE} .+' + '$'),
            CallbackQueryHandler(send_all_lab_files, pattern='^' + f'{user_constants.LAB} \d+' + '$'),
        ],
    },
    fallbacks=[],
    persistent=True,
    name='notifications_conv',
    per_message=True,
    allow_reentry=True,
)