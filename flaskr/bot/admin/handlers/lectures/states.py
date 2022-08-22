from telegram.ext import MessageHandler, Filters
from flaskr.bot.admin import admin_constants
import flaskr.bot.admin.handlers.courses as courses
import flaskr.bot.admin.handlers.courses.course as course
import flaskr.bot.admin.handlers.lectures  as lectures
import flaskr.bot.admin.handlers.lectures.lecture  as lecture
import flaskr.bot.admin.handlers.lectures.lecture.file  as lecture_file
import flaskr.bot.admin.handlers.lectures.lecture.receivers as lecture_receivers
import flaskr.bot.admin.handlers.lectures.lecture.publishers as lecture_publishers


states = {

    admin_constants.LECTURES_LIST: [
        MessageHandler(Filters.regex(f'المحاضرة رقم: .*'), lectures.list_lecture_files),
        MessageHandler(Filters.regex(f'رجوع'), courses.to_edit_course),
        MessageHandler(Filters.regex(f'اضافة محاضرة'), lectures.add_lecture),
    ],

    admin_constants.LECTURE_OPTIONS: [
        MessageHandler(Filters.regex(f'حذف المحاضرة'), lecture.delete_lecture),
        MessageHandler(Filters.regex(f'تعديل رقم المحاضرة: \d+'),
                        lectures.lecture.edit_lecture_number),
        MessageHandler(Filters.regex(f'اضافة ملف'), lecture.add_file),
        MessageHandler(Filters.regex(f'نشر'), lecture.publish),
        MessageHandler(Filters.regex(f'رجوع'), course.list_lectures),
        MessageHandler(Filters.text & ~ Filters.command, lecture.edit_file),
    ],

    admin_constants.LECTURE_FILE_OPTIONS: [
        MessageHandler(Filters.regex(f'حذف الملف'), lecture_file.delete_file),
        MessageHandler(Filters.regex(f'عرض'), lecture_file.send_file),
        MessageHandler(Filters.regex(f'رجوع'), lectures.to_list_lecture_files),
    ],

    admin_constants.RECIEVE_LECTURE_NUMBER: [
        MessageHandler(Filters.text & ~(Filters.command),
                        lecture_receivers.recieve_lecture_number),
    ],

    admin_constants.RECIEVIE_LECTURE_FILE: [
        MessageHandler((Filters.document | Filters.video | Filters.entity('url')) &
                        ~ Filters.command, lecture_receivers.recieve_lecture_file),
        MessageHandler(Filters.regex('رجوع'), lectures.list_lecture_files)
    ],

    admin_constants.PUBLISH_LECTURE: [
        MessageHandler(Filters.regex(f'ارسل تنبيه'), lecture_publishers.publish_with_notification),
        MessageHandler(Filters.regex(f'نشر بصمت'), lecture_publishers.publish_silently),
        MessageHandler(Filters.regex(f'رجوع'), lectures.to_list_lecture_files),
    ],
}