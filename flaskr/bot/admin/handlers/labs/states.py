from telegram.ext import MessageHandler, Filters
from flaskr.bot.admin import admin_constants
import flaskr.bot.admin.handlers.courses as courses
import flaskr.bot.admin.handlers.courses.course as course
import flaskr.bot.admin.handlers.labs as labs
import flaskr.bot.admin.handlers.labs.lab as lab
import flaskr.bot.admin.handlers.labs.lab.receivers as lab_receivers
import flaskr.bot.admin.handlers.labs.lab.publishers as lab_publishers
import flaskr.bot.admin.handlers.labs.lab.file as lab_file

states = {

        admin_constants.LABS_LIST: [
            MessageHandler(Filters.regex(f'لاب رقم: .*'), labs.list_lab_files),
            MessageHandler(Filters.regex(f'رجوع'), courses.to_edit_course),
            MessageHandler(Filters.regex(f'اضافة لاب'), labs.add_lab),
        ],

        admin_constants.LAB_OPTIONS: [
            MessageHandler(Filters.regex(f'حذف اللاب'), lab.delete_lab),
            MessageHandler(Filters.regex(f'تعديل رقم اللاب: \d+'),
                           labs.lab.edit_lab_number),
            MessageHandler(Filters.regex(f'اضافة ملف'), lab.add_file),
            MessageHandler(Filters.regex(f'نشر'), lab.publish),
            MessageHandler(Filters.regex(f'رجوع'), course.list_labs),
            MessageHandler(Filters.text & ~ Filters.command, lab.edit_file),
        ],

        admin_constants.LAB_FILE_OPTIONS: [
            MessageHandler(Filters.regex(f'حذف الملف'), lab_file.delete_file),
            MessageHandler(Filters.regex(f'عرض'), lab_file.send_file),
            MessageHandler(Filters.regex(f'رجوع'), labs.list_lab_files),
        ],

        admin_constants.RECIEVE_LAB_NUMBER: [
            MessageHandler(Filters.text & ~(Filters.command),
                           lab_receivers.recieve_lab_number),
        ],

        admin_constants.RECIEVIE_LAB_FILE: [
            MessageHandler((Filters.document | Filters.video | Filters.entity('url')) &
                           ~ Filters.command, lab_receivers.recieve_lab_file),
            MessageHandler(Filters.regex('رجوع'), labs.list_lab_files)
        ],
    
        admin_constants.PUBLISH_LAB: [
            MessageHandler(Filters.regex(f'ارسل تنبيه'), lab_publishers.publish_with_notification),
            MessageHandler(Filters.regex(f'نشر بصمت'), lab_publishers.publish_silently),
            MessageHandler(Filters.regex(f'رجوع'), labs.list_lab_files),
        ],
}