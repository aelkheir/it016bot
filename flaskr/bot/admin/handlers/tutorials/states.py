from telegram.ext import MessageHandler, Filters
from flaskr.bot.admin import admin_constants
import flaskr.bot.admin.handlers.courses as courses
import flaskr.bot.admin.handlers.courses.course as course
import flaskr.bot.admin.handlers.tutorials as tutorials
import flaskr.bot.admin.handlers.tutorials.tutorial as tutorial
import flaskr.bot.admin.handlers.tutorials.tutorial.receivers as tutorial_receivers
import flaskr.bot.admin.handlers.tutorials.tutorial.publishers as tutorial_publishers
import flaskr.bot.admin.handlers.tutorials.tutorial.file as tutorial_file

states = {

        admin_constants.TUTORIALS_LIST: [
            MessageHandler(Filters.regex(f'تمرين رقم: .*'), tutorials.list_tutorial_files),
            MessageHandler(Filters.regex(f'رجوع'), courses.to_edit_course),
            MessageHandler(Filters.regex(f'اضافة تمرين'), tutorials.add_tutorial),
        ],

        admin_constants.TUTORIAL_OPTIONS: [
            MessageHandler(Filters.regex(f'حذف التمرين'), tutorial.delete_tutorial),
            MessageHandler(Filters.regex(f'تعديل رقم التمرين: \d+'),
                           tutorial.edit_tutorial_number),
            MessageHandler(Filters.regex(f'اضافة ملف'), tutorial.add_file),
            MessageHandler(Filters.regex(f'نشر'), tutorial.publish),
            MessageHandler(Filters.regex(f'رجوع'), course.list_tutorials),
            MessageHandler(Filters.text & ~ Filters.command, tutorial.edit_file),
        ],

        admin_constants.TUTORIAL_FILE_OPTIONS: [
            MessageHandler(Filters.regex(f'حذف الملف'), tutorial_file.delete_file),
            MessageHandler(Filters.regex(f'عرض'), tutorial_file.send_file),
            MessageHandler(Filters.regex(f'رجوع'), tutorials.list_tutorial_files),
        ],

        admin_constants.RECIEVE_TUTORIAL_NUMBER: [
            MessageHandler(Filters.text & ~(Filters.command),
                           tutorial_receivers.recieve_tutorial_number),
        ],

        admin_constants.RECIEVIE_TUTORIAL_FILE: [
            MessageHandler((Filters.document | Filters.video | Filters.entity('url')) &
                           ~ Filters.command, tutorial_receivers.recieve_tutorial_file),
            MessageHandler(Filters.regex('رجوع'), tutorials.list_tutorial_files)
        ],
    
        admin_constants.PUBLISH_TUTTORIAL: [
            MessageHandler(Filters.regex(f'ارسل تنبيه'), tutorial_publishers.publish_with_notification),
            MessageHandler(Filters.regex(f'نشر بصمت'), tutorial_publishers.publish_silently),
            MessageHandler(Filters.regex(f'رجوع'), tutorials.list_tutorial_files),
        ],
}