from flaskr.bot.owner.handlers.user_options import delete_user, subscribe_user, unsubscribe_user
from flaskr.bot.owner.handlers.admin_options import delete_admin
from flaskr.bot.owner.handlers.admin_list import view_admin, add_admin
from flaskr.bot.utils.cancel_conversation import cancel_conversation
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler
from telegram.ext.filters import Filters
import flaskr.bot.owner.owner_constants as constants
from flaskr.bot.owner.handlers.choice import list_admins, list_users
from flaskr.bot.owner.handlers.recieve_new_admin import recieve_new_admin
from flaskr.bot.owner.handlers.owner_handler import owner_handler
from flaskr.bot.owner.handlers.view_user import  view_all_users, view_user


owner_conv = ConversationHandler(
    entry_points=[CommandHandler('manageusers', owner_handler)],
    states={
        constants.CHOICE: [
            MessageHandler(Filters.regex(f'المستخدمين'), list_users),
            MessageHandler(Filters.regex(f'المدراء'), list_admins),
        ],

        constants.USER_VIEW: [
            MessageHandler(Filters.regex(f'رجوع'), owner_handler),
            MessageHandler(Filters.regex(f'عرض الكل: .*'), view_all_users),
            MessageHandler(Filters.text & ~ Filters.command, view_user),
        ],

        constants.ADMINS_LIST: [
            MessageHandler(Filters.regex(f'اضافة مدير'), add_admin),
            MessageHandler(Filters.regex(f'رجوع'), owner_handler),
            MessageHandler(Filters.text & ~ Filters.command, view_admin),
        ],

        constants.RECIEVE_NEW_ADMIN: [
            MessageHandler(Filters.forwarded & ~ Filters.command, recieve_new_admin),
        ],

        constants.USER_OPTIONS: [
            MessageHandler(Filters.regex(f'رجوع'), list_users),
            MessageHandler(Filters.regex(f'حذف المستخدم'), delete_user),
            MessageHandler(Filters.regex(f'^اشتراك$'), subscribe_user),
            MessageHandler(Filters.regex(f'^الغاء الاشتراك$'), unsubscribe_user),
        ],

        constants.ADMIN_OPTIONS: [
            MessageHandler(Filters.regex(f'حذف من المدراء'), delete_admin),
            MessageHandler(Filters.regex(f'رجوع'), list_admins),
        ],
    },

    fallbacks=[MessageHandler(Filters.command, cancel_conversation)],
    persistent=True,
    name="owner_conv",
    allow_reentry=True
)