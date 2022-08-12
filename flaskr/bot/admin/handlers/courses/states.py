from telegram.ext import MessageHandler, Filters
from flaskr.bot.admin import admin_constants
import flaskr.bot.admin.handlers.courses as courses
import flaskr.bot.admin.handlers.courses.receivers as courses_receivers
import flaskr.bot.admin.handlers.courses.course as course
import flaskr.bot.admin.handlers.courses.course.receivers as course_receivers
from flaskr.bot.admin.handlers.admin_handler import admin_handler
import flaskr.bot.admin.handlers.semesters  as semesters


states = {

    admin_constants.COURSE_LIST: [
        MessageHandler(Filters.text & ~ Filters.command, courses.edit_course)
    ],

    admin_constants.COURSE_OPTIONS: [
        MessageHandler(Filters.regex(f'المحاضرات'), course.list_lectures),
        MessageHandler(Filters.regex(f'المراجع'), course.list_refferences),
        MessageHandler(Filters.regex(f'اللابات'), course.list_labs),
        MessageHandler(Filters.regex(f'الامتحانات'), course.list_exams),
        MessageHandler(Filters.regex(f'التساليم'), course.list_assignments),
        MessageHandler(Filters.regex(f'تعديل\sال(.+)'), course.edit_name_symbol),
        MessageHandler(Filters.regex(f'سمستر:\s.+'), course.edit_course_semester),
        MessageHandler(Filters.regex(f'حذف المادة'),
                        course.confirm_delete_course),
        MessageHandler(Filters.regex(f'^رجوع$'), admin_handler),
        MessageHandler(Filters.regex(f'رجوع لسمستر.*'), semesters.edit_semester),
    ],

    admin_constants.RECIEVE_NAME_SYMBOL: [
        MessageHandler(Filters.text & ~(
            Filters.command), course_receivers.recieve_name_symbol)
    ],

    admin_constants.RECIEVE_COURSE_SEMESTER: [
        MessageHandler(Filters.regex(f'سمستر\s(\d+)(\s.*)?'), course_receivers.recieve_course_semester),
        MessageHandler(Filters.regex(f'رجوع'), courses.edit_course)
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
