import functools
from flaskr.bot.user.handlers.list_semester_courses import list_semester_courses
from flaskr.bot.user.handlers.stage_foure import send_all_lab_files
from telegram.ext import CallbackQueryHandler, ConversationHandler, Filters
import flaskr.bot.user.user_constants as constants
from flaskr.bot.user.handlers.archive import list_semesters
from flaskr.bot.user.handlers.start_over import start_over
from flaskr.bot.user.handlers.stage_three import list_lab_files, send_all_course_exams, send_all_course_refferences, send_all_lecture_files, send_course_exam, send_course_refference, send_file, send_all_labs
from flaskr.bot.user.handlers.stage_two import  list_course_exams, list_course_labs, list_lecture_files, send_all_lectures, list_course_refferences
from flaskr.bot.user.handlers.course_overview import  course_overview



user_conv = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(course_overview, pattern='^' + f'{constants.COURSE} \d+' + '$'),
        CallbackQueryHandler(list_semester_courses, pattern='^' + f'{constants.SEMESTER} .+' + '$'),
    ],
    states={
        constants.COURSE_OVERVIEW: [
            CallbackQueryHandler(course_overview, pattern='^' + f'{constants.COURSE} \d+' + '$'),
        ],

        constants.SEMESTER_LIST: [
        CallbackQueryHandler(list_semester_courses, pattern='^' + f'{constants.SEMESTER} .+' + '$'),
        ],

        constants.STAGE_TWO: [
            CallbackQueryHandler(list_lecture_files, pattern='^' + f'{constants.LECTURE} \d+' + '$'),
            CallbackQueryHandler(send_all_lectures, pattern='^' + f'{constants.LECTURES} \d+' + '$'),
            CallbackQueryHandler(list_course_labs, pattern='^' + f'\d+ {constants.LABS}' + '$'),
            CallbackQueryHandler(list_course_refferences, pattern='^' + f'\d+ {constants.REFFERENCES}' + '$'),
            CallbackQueryHandler(list_course_exams, pattern='^' + f'\d+ {constants.EXAMS}' + '$'),
            CallbackQueryHandler(start_over, pattern='^' + constants.SUBJECT_LIST + '$'),
            CallbackQueryHandler(list_semester_courses, pattern='^' + f'{constants.SEMESTER} .+' + '$'),
        ],

        constants.ARCHIVED_SEMESTER: [
            CallbackQueryHandler(
                functools.partial(course_overview, from_archive=True),
                pattern='^' + f'{constants.COURSE} \d+' + '$'
            ),
            CallbackQueryHandler(list_semesters, pattern='^' + f'{constants.ARCHIVE}' + '$'),
        ],

        constants.STAGE_THREE: [
            CallbackQueryHandler(list_lab_files, pattern='^' + f'{constants.LAB} \d+' + '$'),
            CallbackQueryHandler(send_all_labs, pattern='^' + f'{constants.LABS} \d+' + '$'),
            CallbackQueryHandler(send_file, pattern='^' + f'{constants.FILE} .+' + '$'),
            CallbackQueryHandler(send_all_lecture_files, pattern='^' + f'{constants.LECTURE} \d+' + '$'),
            CallbackQueryHandler(send_course_refference, pattern='^' + f'{constants.REFFERENCE} \d+' + '$'),
            CallbackQueryHandler(send_all_course_refferences, pattern='^' + f'{constants.REFFERENCES} \d+' + '$'),
            CallbackQueryHandler(send_course_exam, pattern='^' + f'{constants.EXAM} \d+' + '$'),
            CallbackQueryHandler(send_all_course_exams, pattern='^' + f'{constants.EXAMS} \d+' + '$'),
            CallbackQueryHandler(course_overview, pattern='^' + f'{constants.COURSE} \d+' + '$'),
        ],

        constants.STAGE_FOURE: [
            CallbackQueryHandler(list_course_labs, pattern='^' + f'\d+ {constants.LABS}' + '$'),
            CallbackQueryHandler(send_file, pattern='^' + f'{constants.FILE} .+' + '$'),
            CallbackQueryHandler(send_all_lab_files, pattern='^' + f'{constants.LAB} \d+' + '$'),
        ],
    },
    fallbacks=[],
    persistent=True,
    name='user_conv',
    per_message=True,
)