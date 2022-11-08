from telegram.ext import MessageHandler, Filters
from flaskr.bot.admin import admin_constants
import flaskr.bot.admin.handlers.courses as courses
import flaskr.bot.admin.handlers.courses.course as course
import flaskr.bot.admin.handlers.sheets as sheets
import flaskr.bot.admin.handlers.sheets.file as sheet_file
import flaskr.bot.admin.handlers.sheets.receivers as sheets_receivers


states = {

        admin_constants.SHEETS_LIST: [
            MessageHandler(Filters.regex(f'اضافة شيت'), sheets.add_sheet),
            MessageHandler(Filters.regex(f'رجوع'), courses.to_edit_course),
            MessageHandler(Filters.text & ~ Filters.command, sheets.edit_sheet),
        ],

        admin_constants.SHEET_FILE_OPTIONS: [
            MessageHandler(Filters.regex(f'حذف الشيت'), sheet_file.delete_file),
            MessageHandler(Filters.regex(f'عرض'), sheet_file.send_sheet),
            MessageHandler(Filters.regex(f'رجوع'), course.list_sheets),
        ],

        admin_constants.RECIEVE_COURSE_SHEET: [
            MessageHandler(Filters.document & ~
                           Filters.command, sheets_receivers.recieve_course_sheet),
            MessageHandler(Filters.regex('رجوع'), course.list_sheets)
        ],

}
