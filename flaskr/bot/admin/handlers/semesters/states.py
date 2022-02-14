from telegram.ext import MessageHandler, Filters
import flaskr.bot.admin.admin_constants as constants
import flaskr.bot.admin.handlers.courses as  courses
from flaskr.bot.admin.handlers.edit_archive import edit_archive
from flaskr.bot.admin.handlers.semesters import edit_semester, add_semester
from flaskr.bot.admin.handlers.semesters.semester import delete_semester, edit_semester_number, set_to_current_semester 
from flaskr.bot.admin.handlers.semesters.semester.receivers import receive_semester_number

states = {

    constants.SEMESTER_LIST: [
        MessageHandler(Filters.regex(f'سمستر\s\d+'), edit_semester),
        MessageHandler(Filters.regex(f'اضافة سمستر'), add_semester),
    ],

    constants.SEMESTER_OPTIONS: [
        MessageHandler(Filters.regex(f'اضافة مادة'), courses.add_course),

        MessageHandler(Filters.regex(f'وضع للحالي'), set_to_current_semester),

        MessageHandler(Filters.regex(f'تعديل رقم السمستر: \d+'),
                        edit_semester_number),
        MessageHandler(Filters.regex(f'حذف السمستر'),delete_semester),

        MessageHandler(Filters.regex(f'رجوع'), edit_archive),

        MessageHandler(Filters.text & ~ Filters.command, courses.edit_course),
    ],

    constants.RECIEVE_SEMESTER_NUMBER: [
        MessageHandler(Filters.text & ~(Filters.command),
                        receive_semester_number),
    ],


}