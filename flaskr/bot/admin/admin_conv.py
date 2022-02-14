from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters
from flaskr.bot.admin.handlers.edit_archive import edit_archive
from flaskr.bot.utils.cancel_conversation import cancel_conversation
from flaskr.bot.admin.handlers.admin_handler import admin_handler
from flaskr.bot.admin.handlers.semesters.states import states as semesters_states
from flaskr.bot.admin.handlers.courses.states import states as courses_states
from flaskr.bot.admin.handlers.lectures.states import states as lectures_states
from flaskr.bot.admin.handlers.labs.states import states as labs_states
from flaskr.bot.admin.handlers.exams.states import states as exams_states
from flaskr.bot.admin.handlers.references.states import states as references_states



admin_conv = ConversationHandler(
    entry_points=[
        CommandHandler('editcourses', admin_handler),
        CommandHandler('editarchive', edit_archive),
    ],
    states={
        **semesters_states,
        **courses_states,
        **lectures_states,
        **labs_states,
        **exams_states,
        **references_states,
    },
    fallbacks=[MessageHandler(Filters.command, cancel_conversation)],
    persistent=True,
    name="admin_conv",
    allow_reentry=True
)
