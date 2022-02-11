from telegram.ext import MessageHandler, Filters
import flaskr.bot.owner.owner_constants as constants
from flaskr.bot.owner.handlers.manage_semesters import manage_semesters
from flaskr.bot.owner.handlers.semesters import edit_semester, add_semester
from flaskr.bot.owner.handlers.semesters.semester import delete_semester, edit_semester_number, add_to_archive, remove_from_archive 
from flaskr.bot.owner.handlers.semesters.semester.receivers import receive_semester_number

states = {

    constants.SEMESTER_LIST: [
        MessageHandler(Filters.regex(f'سمستر\s\d+'), edit_semester),
        MessageHandler(Filters.regex(f'اضافة سمستر'), add_semester),
    ],

    constants.SEMESTER_OPTIONS: [
        MessageHandler(Filters.regex(f'اضف للارشيف'), add_to_archive),
        MessageHandler(Filters.regex(f'استخرج من الارشيف'), remove_from_archive),

        MessageHandler(Filters.regex(f'تعديل رقم السمستر: \d+'),
                        edit_semester_number),
        MessageHandler(Filters.regex(f'حذف السمستر'),delete_semester),

        MessageHandler(Filters.regex(f'رجوع'), manage_semesters),
    ],

    constants.RECIEVE_SEMESTER_NUMBER: [
        MessageHandler(Filters.text & ~(Filters.command),
                        receive_semester_number),
    ],


}