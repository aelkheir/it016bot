from telegram.ext import MessageHandler, Filters
from flaskr.bot.admin import admin_constants
import flaskr.bot.admin.handlers.courses as courses
import flaskr.bot.admin.handlers.courses.course as course
import flaskr.bot.admin.handlers.exams as exams
import flaskr.bot.admin.handlers.exams.exam as exam
import flaskr.bot.admin.handlers.exams.exam.file as exam_file
import flaskr.bot.admin.handlers.exams.exam.receivers as exam_receivers
import flaskr.bot.admin.handlers.exams.receivers as exams_receivers


states = {

    admin_constants.EXAMS_LIST: [
        MessageHandler(Filters.regex(f'اضافة امتحان'), exams.add_exam),
        MessageHandler(Filters.regex(f'رجوع'), courses.to_edit_course),
        MessageHandler(Filters.text & ~ Filters.command, exams.edit_exam),
    ],

    admin_constants.EXAM_OPTIONS: [
        MessageHandler(Filters.regex(f'حذف الامتحان'), exam.delete_exam),
        MessageHandler(Filters.regex(f'تعديل الاسم'), exam.edit_exam_name),
        MessageHandler(Filters.regex(f'اضافة ملف'), exam.add_file),
        MessageHandler(Filters.regex(f'رجوع'), course.list_exams),
        MessageHandler(Filters.text & ~ Filters.command, exam.edit_file),
    ],

    admin_constants.EXAM_FILE_OPTIONS: [
        MessageHandler(Filters.regex(f'حذف الملف'), exam_file.delete_file),
        MessageHandler(Filters.regex(f'عرض'), exam_file.send_file),
        MessageHandler(Filters.regex(f'رجوع'), exams.edit_exam),
    ],

    admin_constants.RECIEVE_EXAM_NAME: [
        MessageHandler(Filters.text & ~(
            Filters.command), exams_receivers.recieve_exam_name),
    ],

    admin_constants.RECIEVE_EXAM_FILE: [
        MessageHandler((Filters.document | Filters.photo) & ~ 
                        Filters.command, exam_receivers.recieve_exam_file),
        MessageHandler(Filters.regex('رجوع'), exams.edit_exam)
    ],
}