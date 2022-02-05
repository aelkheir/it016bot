from telegram.ext import MessageHandler, Filters
from flaskr.bot.admin import admin_constants
import flaskr.bot.admin.handlers.courses as courses
import flaskr.bot.admin.handlers.courses.course as course
import flaskr.bot.admin.handlers.references as references
import flaskr.bot.admin.handlers.references.file as reference_file
import flaskr.bot.admin.handlers.references.receivers as references_receivers


states = {

        admin_constants.REFFERENCES_LIST: [
            MessageHandler(Filters.regex(f'اضافة مرجع'), references.add_refference),
            MessageHandler(Filters.regex(f'رجوع'), courses.to_edit_course),
            MessageHandler(Filters.text & ~ Filters.command, references.edit_refference),
        ],

        admin_constants.REFFERENCE_FILE_OPTIONS: [
            MessageHandler(Filters.regex(f'حذف المرجع'), reference_file.delete_refference),
            MessageHandler(Filters.regex(f'عرض'), reference_file.send_refference),
            MessageHandler(Filters.regex(f'رجوع'), course.list_refferences),
        ],

        admin_constants.RECIEVE_COURSE_REF: [
            MessageHandler(Filters.document & ~
                           Filters.command, references_receivers.recieve_course_ref),
            MessageHandler(Filters.regex('رجوع'), course.list_refferences)
        ],

}
