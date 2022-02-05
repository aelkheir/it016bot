from telegram.ext import MessageHandler, Filters
from flaskr.bot.admin import admin_constants
import flaskr.bot.admin.handlers.courses as courses
import flaskr.bot.admin.handlers.courses.receivers as courses_receivers
import flaskr.bot.admin.handlers.courses.course as course
import flaskr.bot.admin.handlers.courses.course.receivers as course_receivers
from flaskr.bot.admin.handlers.admin_handler import admin_handler


states = {

    admin_constants.COURSE_LIST: [
        MessageHandler(Filters.regex(f'اضافة مادة'), courses.add_course),
        MessageHandler(Filters.text & ~ Filters.command, courses.edit_course)
    ],

    admin_constants.COURSE_OPTIONS: [
        MessageHandler(Filters.regex(f'المحاضرات'), course.list_lectures),
        MessageHandler(Filters.regex(f'المراجع'), course.list_refferences),
        MessageHandler(Filters.regex(f'اللابات'), course.list_labs),
        MessageHandler(Filters.regex(f'الامتحانات'), course.list_exams),
        MessageHandler(Filters.regex(f'تعديل\sال(.+)'), course.edit_name_symbol),
        MessageHandler(Filters.regex(f'حذف المادة'),
                        course.confirm_delete_course),
        MessageHandler(Filters.regex(f'رجوع'), admin_handler)
    ],

    admin_constants.RECIEVE_NAME_SYMBOL: [
        MessageHandler(Filters.text & ~(
            Filters.command), course_receivers.recieve_name_symbol)
    ],

    admin_constants.RECIEVE_NEW_COURSE: [
        MessageHandler(Filters.text & ~(
            Filters.command), courses_receivers.recieve_new_course),
    ],

    admin_constants.CONFIRM_COURSE_DELETION: [
        MessageHandler(Filters.text & ~(
            Filters.command), course_receivers.apply_delete_course),
    ],

}
