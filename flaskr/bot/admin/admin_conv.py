from flaskr.bot.admin.handlers.recieve_exam_name import recieve_exam_name
from flaskr.bot.admin.handlers.revieve_lab_file import recieve_lab_file
from flaskr.bot.admin.handlers.recieve_lab_number import recieve_lab_number
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters
from flaskr.bot.utils.cancel_conversation import cancel_conversation
import flaskr.bot.admin.handlers.course_overview as course_overview
from flaskr.bot.admin.handlers.admin_handler import admin_handler
import flaskr.bot.admin.handlers.course_options as course_options
from flaskr.bot.admin.handlers.recieve_name_symbol import recieve_name_symbol
import flaskr.bot.admin.handlers.lectures_list as lectures_list
import flaskr.bot.admin.handlers.labs_list as labs_list
import flaskr.bot.admin.handlers.exams_list as exams_list
import flaskr.bot.admin.handlers.exam_options as exam_options
import flaskr.bot.admin.handlers.lecture_options  as lecture_options
import flaskr.bot.admin.handlers.lab_options  as lab_options
import flaskr.bot.admin.handlers.refference_options as refference_options
from flaskr.bot.admin.handlers.confirm_course_deletion import apply_delete_course
from flaskr.bot.admin.handlers.recieve_lecture_number import recieve_lecture_number
from flaskr.bot.admin.handlers.recieve_exam_file import recieve_exam_file
from flaskr.bot.admin.handlers.recieve_course_ref import recieve_course_ref
from flaskr.bot.admin.handlers.recieve_lecture_file import recieve_lecture_file
from flaskr.bot.admin.handlers.recieve_new_course import recieve_new_course
import flaskr.bot.admin.handlers.refferences_list as refferences_list
import flaskr.bot.admin.handlers.lecture_file_options as lecture_file_options
import flaskr.bot.admin.handlers.lab_file_options as lab_file_options
import flaskr.bot.admin.handlers.exam_file_options as exam_file_options
from flaskr.bot.admin import admin_constants


admin_conv = ConversationHandler(
    entry_points=[CommandHandler('editcourses', admin_handler)],
    states={
        admin_constants.COURSE_OVERVIEW: [
            MessageHandler(Filters.regex(f'اضافة مادة'), course_overview.add_course),
            MessageHandler(Filters.text & ~ Filters.command, course_overview.course_overview)
        ],

        admin_constants.COURSE_OPTIONS: [
            MessageHandler(Filters.regex(f'المحاضرات'), course_options.list_lectures),
            MessageHandler(Filters.regex(f'المراجع'), course_options.list_refferences),
            MessageHandler(Filters.regex(f'اللابات'), course_options.list_labs),
            MessageHandler(Filters.regex(f'الامتحانات'), course_options.list_exams),
            MessageHandler(Filters.regex(f'تعديل\sال(.+)'), course_options.edit_name_symbol),
            MessageHandler(Filters.regex(f'حذف المادة'),
                           course_options.confirm_delete_course),
            MessageHandler(Filters.regex(f'رجوع'), admin_handler)
        ],

        admin_constants.LECTURES_LIST: [
            MessageHandler(Filters.regex(f'المحاضرة رقم: .*'), lectures_list.list_lecture_files),
            MessageHandler(Filters.regex(f'رجوع'), course_overview.to_course_overview),
            MessageHandler(Filters.regex(f'اضافة محاضرة'), lectures_list.add_lecture),
        ],

        admin_constants.LABS_LIST: [
            MessageHandler(Filters.regex(f'لاب رقم: .*'), labs_list.list_lab_files),
            MessageHandler(Filters.regex(f'رجوع'), course_overview.to_course_overview),
            MessageHandler(Filters.regex(f'اضافة لاب'), labs_list.add_lab),
        ],

        admin_constants.REFFERENCES_LIST: [
            MessageHandler(Filters.regex(f'اضافة مرجع'), refferences_list.add_refference),
            MessageHandler(Filters.regex(f'رجوع'), course_overview.to_course_overview),
            MessageHandler(Filters.text & ~ Filters.command, refferences_list.edit_refference),
        ],

        admin_constants.LECTURE_OPTIONS: [
            MessageHandler(Filters.regex(f'حذف المحاضرة'), lecture_options.delete_lecture),
            MessageHandler(Filters.regex(f'تعديل رقم المحاضرة: \d+'),
                           lecture_options.edit_lecture_number),
            MessageHandler(Filters.regex(f'اضافة ملف'), lecture_options.add_file),
            MessageHandler(Filters.regex(f'رجوع'), course_options.list_lectures),
            MessageHandler(Filters.text & ~ Filters.command, lecture_options.edit_file),
        ],

        admin_constants.LAB_OPTIONS: [
            MessageHandler(Filters.regex(f'حذف اللاب'), lab_options.delete_lab),
            MessageHandler(Filters.regex(f'تعديل رقم اللاب: \d+'),
                           lab_options.edit_lab_number),
            MessageHandler(Filters.regex(f'اضافة ملف'), lab_options.add_file),
            MessageHandler(Filters.regex(f'رجوع'), course_options.list_labs),
            MessageHandler(Filters.text & ~ Filters.command, lab_options.edit_file),
        ],

        admin_constants.EXAMS_LIST: [
            MessageHandler(Filters.regex(f'اضافة امتحان'), exams_list.add_exam),
            MessageHandler(Filters.regex(f'رجوع'), course_overview.to_course_overview),
            MessageHandler(Filters.text & ~ Filters.command, exams_list.edit_exam),
        ],

        admin_constants.EXAM_OPTIONS: [
            MessageHandler(Filters.regex(f'حذف الامتحان'), exam_options.delete_exam),
            MessageHandler(Filters.regex(f'تعديل الاسم'), exam_options.edit_exam_name),
            MessageHandler(Filters.regex(f'اضافة ملف'), exam_options.add_file),
            MessageHandler(Filters.regex(f'رجوع'), course_options.list_exams),
            MessageHandler(Filters.text & ~ Filters.command, exam_options.edit_file),
        ],

        admin_constants.LECTURE_FILE_OPTIONS: [
            MessageHandler(Filters.regex(f'حذف الملف'), lecture_file_options.delete_file),
            MessageHandler(Filters.regex(f'عرض'), lecture_file_options.send_file),
            MessageHandler(Filters.regex(f'رجوع'), lectures_list.to_list_lecture_files),
        ],

        admin_constants.LAB_FILE_OPTIONS: [
            MessageHandler(Filters.regex(f'حذف الملف'), lab_file_options.delete_file),
            MessageHandler(Filters.regex(f'عرض'), lab_file_options.send_file),
            MessageHandler(Filters.regex(f'رجوع'), labs_list.list_lab_files),
        ],

        admin_constants.EXAM_FILE_OPTIONS: [
            MessageHandler(Filters.regex(f'حذف الملف'), exam_file_options.delete_file),
            MessageHandler(Filters.regex(f'عرض'), exam_file_options.send_file),
            MessageHandler(Filters.regex(f'رجوع'), exams_list.edit_exam),
        ],

        admin_constants.REFFERENCE_OPTIONS: [
            MessageHandler(Filters.regex(f'حذف المرجع'), refference_options.delete_refference),
            MessageHandler(Filters.regex(f'عرض'), refference_options.send_refference),
            MessageHandler(Filters.regex(f'رجوع'), course_options.list_refferences),
        ],

        admin_constants.RECIEVE_NAME_SYMBOL: [
            MessageHandler(Filters.text & ~(
                Filters.command), recieve_name_symbol),
        ],

        admin_constants.RECIEVE_LECTURE_NUMBER: [
            MessageHandler(Filters.text & ~(Filters.command),
                           recieve_lecture_number),
        ],

        admin_constants.RECIEVE_LAB_NUMBER: [
            MessageHandler(Filters.text & ~(Filters.command),
                           recieve_lab_number),
        ],

        admin_constants.RECIEVE_NEW_COURSE: [
            MessageHandler(Filters.text & ~(
                Filters.command), recieve_new_course),
        ],

        admin_constants.CONFIRM_COURSE_DELETION: [
            MessageHandler(Filters.text & ~(
                Filters.command), apply_delete_course),
        ],

        admin_constants.RECIEVIE_LAB_FILE: [
            MessageHandler((Filters.document | Filters.video | Filters.entity('url')) &
                           ~ Filters.command, recieve_lab_file),
            MessageHandler(Filters.regex('رجوع'), labs_list.list_lab_files)
        ],


        admin_constants.RECIEVIE_LECTURE_FILE: [
            MessageHandler((Filters.document | Filters.video | Filters.entity('url')) &
                           ~ Filters.command, recieve_lecture_file),
            MessageHandler(Filters.regex('رجوع'), lectures_list.list_lecture_files)
        ],

        admin_constants.RECIEVE_COURSE_REF: [
            MessageHandler(Filters.document & ~
                           Filters.command, recieve_course_ref),
            MessageHandler(Filters.regex('رجوع'), course_options.list_refferences)
        ],

        admin_constants.RECIEVE_EXAM_NAME: [
            MessageHandler(Filters.text & ~(
                Filters.command), recieve_exam_name),
        ],

        admin_constants.RECIEVE_EXAM_FILE: [
            MessageHandler((Filters.document | Filters.photo) & ~ 
                            Filters.command, recieve_exam_file),
            MessageHandler(Filters.regex('رجوع'), exams_list.edit_exam)
        ],
    },
    fallbacks=[MessageHandler(Filters.command, cancel_conversation)],
    persistent=True,
    name="admin_conv",
    allow_reentry=True
)
