from telegram.ext import MessageHandler, Filters
from flaskr.bot.admin import admin_constants
import flaskr.bot.admin.handlers.courses as courses
import flaskr.bot.admin.handlers.courses.course as course
import flaskr.bot.admin.handlers.assignments as assignments
import flaskr.bot.admin.handlers.assignments.assignment as assignment
import flaskr.bot.admin.handlers.assignments.assignment.receivers as assignment_receivers
import flaskr.bot.admin.handlers.assignments.assignment.file as assignment_file
import flaskr.bot.admin.handlers.assignments.assignment.publishers as assignment_publishers

states = {

        admin_constants.ASSIGNMENTS_LIST: [
            MessageHandler(Filters.regex(f'تسليم رقم: .*'), assignments.list_assignment_files),
            MessageHandler(Filters.regex(f'رجوع'), courses.to_edit_course),
            MessageHandler(Filters.regex(f'اضافة تسليم'), assignments.add_assignment),
        ],

        admin_constants.ASSIGNMENT_OPTIONS: [
            MessageHandler(Filters.regex(f'حذف التسليم'), assignment.delete_assignment),
            MessageHandler(Filters.regex(f'تعديل رقم التسليم: \d+'),
                           assignment.edit_assignment_number),
            MessageHandler(Filters.regex(f'اضافة ملف'), assignment.add_file),
            MessageHandler(Filters.regex(f'نشر'), assignment.publish),
            MessageHandler(Filters.regex(f'رجوع'), course.list_assignments),
            MessageHandler(Filters.text & ~ Filters.command, assignment.edit_file),
        ],

        admin_constants.ASSIGNMENT_FILE_OPTIONS: [
            MessageHandler(Filters.regex(f'حذف الملف'), assignment_file.delete_file),
            MessageHandler(Filters.regex(f'عرض'), assignment_file.send_file),
            MessageHandler(Filters.regex(f'رجوع'), assignments.list_assignment_files),
        ],

        admin_constants.RECIEVE_ASSIGNMENT_NUMBER: [
            MessageHandler(Filters.text & ~(Filters.command),
                           assignment_receivers.recieve_assignment_number),
        ],

        admin_constants.RECIEVIE_ASSIGNMENT_FILE: [
            MessageHandler((Filters.document | Filters.photo ) &
                           ~ Filters.command, assignment_receivers.recieve_assignment_file),
            MessageHandler(Filters.regex('رجوع'), assignments.list_assignment_files)
        ],
        admin_constants.PUBLISH_ASSIGNMENT: [
            MessageHandler(Filters.regex(f'ارسل تنبيه'), assignment_publishers.publish_with_notification),
            MessageHandler(Filters.regex(f'نشر بصمت'), assignment_publishers.publish_silently),
            MessageHandler(Filters.regex(f'رجوع'), assignments.list_assignment_files),
        ],
}