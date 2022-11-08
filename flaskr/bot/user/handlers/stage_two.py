import math
from flaskr.bot.utils.buttons import back_to_course_button
from flaskr.bot.utils.get_user_language import get_user_language
from flaskr.bot.utils.user_required import user_required
from flaskr.models import Assignment, Course, Exam, Lab, Lecture, Tutorial, User
from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from flaskr.bot.user.user_constants import  ASSIGNMENT, EXAM, EXAMS, FILE, LAB, LABS, LECTURE, REFFERENCES, REFFERENCE, SHEET, SHEETS, SHOW_GLOBAL_NOTE, STAGE_THREE, TUTORIAL
from flaskr import db

back_icon ='»'

def list_lecture_files(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)
    language = get_user_language(context.chat_data['language'])

    _, lecture_id = query.data.split(' ')

    lecture = session.query(Lecture).filter(Lecture.id==lecture_id).one()
    course = lecture.course

    keyboard = []

    for document in lecture.documents:
        keyboard.append([
            InlineKeyboardButton(
                f'{document.file_name}',
                callback_data=f'{FILE} {document.id} {document.file_unique_id}'
            )
        ])

    for video in lecture.videos:
        keyboard.append([
            InlineKeyboardButton(
                f'{video.file_name}',
                callback_data=f'{FILE} {video.id} {video.file_unique_id}'
            )
        ])

    for youtube_link in lecture.youtube_links:
        keyboard.append([
            InlineKeyboardButton(f'{youtube_link.video_title}',
            callback_data=f'{FILE} {youtube_link.id}')
        ])

    if len(lecture.documents) + len(lecture.videos) + len(lecture.youtube_links) > 1:
        keyboard.append([InlineKeyboardButton(
            f"{language['download']} {language['all']} {language['files']}".title(),
            callback_data=f'{LECTURE} {lecture.id}')
        ])

    course_name = course.ar_name \
        if user.language == 'ar' \
        else course.en_name
    course_name = course_name if course_name else course.ar_name


    keyboard.append([
        back_to_course_button(language, user.language, course.en_name, course.ar_name, course.id),
    ])

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=f"{course_name}: {language['lecture'].capitalize()} {lecture.lecture_number}",
        reply_markup=reply_markup
    )

    session.close()
    return STAGE_THREE


def send_all_lectures(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)
    language = get_user_language(context.chat_data['language'])

    _, course_id = query.data.split(' ')

    course = session.query(Course).filter(Course.id==course_id).one()

    # read from context
    user_id = context.user_data['user_id']
    user = session.query(User).filter(User.id==user_id).one()

    course_name = course.ar_name \
        if user.language == 'ar' \
        else course.en_name
    course_name = course_name if course_name else course.ar_name

    lectures = session.query(Lecture)\
        .filter(Lecture.course_id == course_id)\
        .order_by(Lecture.lecture_number).all()

    for lecture in lectures:
        query.message.reply_text(
            f"- {course_name}: {language['lecture'].capitalize()} {lecture.lecture_number}"
        )

        for doc in lecture.documents:
            query.bot.sendDocument(query.message.chat.id, document=doc.file_id)
            user.download_count += 1

        for vid in lecture.videos:
            query.bot.sendVideo(query.message.chat.id, video=vid.file_id, caption=vid.file_name)
            user.download_count += 1

        for link in lecture.youtube_links:
            query.bot.sendMessage(query.message.chat.id, text=link.url)
            user.download_count += 1
        
    session.commit()
    session.close()
    return None


def list_course_refferences(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)
    language = get_user_language(context.chat_data['language'])

    course_id, _ = query.data.split(' ')

    course = session.query(Course).filter(Course.id==course_id).one()

    course_name = course.ar_name \
        if user.language == 'ar' \
        else course.en_name
    course_name = course_name if course_name else course.ar_name

    keyboard = []

    for refference in course.refferences:
        keyboard.append([
            InlineKeyboardButton(f'{refference.name}', callback_data=f'{REFFERENCE} {refference.id}')
        ])

    if len(course.refferences) > 1:
        keyboard.append([InlineKeyboardButton(
            f"{language['download']} {language['all']} {language['references']}".title(),
            callback_data=f'{REFFERENCES} {course.id}'),
        ])

    keyboard.append([
        back_to_course_button(language, user.language, course.en_name, course.ar_name, course.id),
    ])

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=f"{course_name}: {language['references'].capitalize()}",
        reply_markup=reply_markup
    )
    return STAGE_THREE

def list_course_sheets(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)
    language = get_user_language(context.chat_data['language'])

    course_id, _ = query.data.split(' ')

    course = session.query(Course).filter(Course.id==course_id).one()

    course_name = course.ar_name \
        if user.language == 'ar' \
        else course.en_name
    course_name = course_name if course_name else course.ar_name

    keyboard = []

    for sheet in course.sheets:
        keyboard.append([
            InlineKeyboardButton(f'{sheet.name}', callback_data=f'{SHEET} {sheet.id}')
        ])

    if len(course.sheets) > 1:
        keyboard.append([InlineKeyboardButton(
            f"{language['download']} {language['all']} {language['sheets']}".title(),
            callback_data=f'{SHEETS} {course.id}'),
        ])

    keyboard.append([
        back_to_course_button(language, user.language, course.en_name, course.ar_name, course.id),
    ])

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text=f"{course_name}: {language['sheets'].capitalize()}",
        reply_markup=reply_markup
    )
    return STAGE_THREE




def list_course_labs(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)
    language = get_user_language(context.chat_data['language'])

    course_id, _ = query.data.split(' ')

    course = session.query(Course).filter(Course.id==course_id).one()

    course_name = course.ar_name \
        if user.language == 'ar' \
        else course.en_name
    course_name = course_name if course_name else course.ar_name

    labs = session.query(Lab)\
        .filter(Lab.course_id == course_id, Lab.published==True)\
        .order_by(Lab.lab_number).all()

    keyboard = []

    for row_index in range(0, math.ceil(len(labs) / 3)):
        row = []
        is_row_full = len(labs) // 3 >= row_index + 1
        row_size = 3 if is_row_full else len(labs) % 3
        row_start = row_index * 3

        for lab_index in range(row_start, row_start + row_size):
            lab = labs[lab_index]
            row.append(InlineKeyboardButton(
                f"{language['lab']} {lab.lab_number}".capitalize(),
                callback_data=f'{LAB} {lab.id}'),
            )

        if user.language == 'ar':
            row.reverse()

        keyboard.append(row)


    keyboard.append([
        back_to_course_button(language, user.language, course.en_name, course.ar_name, course.id),
    ])

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(
        text=f"{course_name}: {language['labs'].capitalize()}",
        reply_markup=reply_markup
    )
    return STAGE_THREE

def list_course_tutorials(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)
    language = get_user_language(context.chat_data['language'])

    course_id, _ = query.data.split(' ')

    course = session.query(Course).filter(Course.id==course_id).one()

    course_name = course.ar_name \
        if user.language == 'ar' \
        else course.en_name
    course_name = course_name if course_name else course.ar_name

    tutorials = session.query(Tutorial)\
        .filter(Tutorial.course_id == course_id, Tutorial.published==True)\
        .order_by(Tutorial.tutorial_number).all()

    keyboard = []

    for row_index in range(0, math.ceil(len(tutorials) / 3)):
        row = []
        is_row_full = len(tutorials) // 3 >= row_index + 1
        row_size = 3 if is_row_full else len(tutorials) % 3
        row_start = row_index * 3

        for lab_index in range(row_start, row_start + row_size):
            tutorial = tutorials[lab_index]
            row.append(InlineKeyboardButton(
                f"{language['tutorial']} {tutorial.tutorial_number}".capitalize(),
                callback_data=f'{TUTORIAL} {tutorial.id}'),
            )

        if user.language == 'ar':
            row.reverse()

        keyboard.append(row)

    keyboard.append([
        back_to_course_button(language, user.language, course.en_name, course.ar_name, course.id),
    ])

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(
        text=f"{course_name}: {language['tutorials'].capitalize()}",
        reply_markup=reply_markup
    )
    return STAGE_THREE


def list_course_assignments(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)
    language = get_user_language(context.chat_data['language'])

    course_id, _ = query.data.split(' ')

    course = session.query(Course).filter(Course.id==course_id).one()

    course_name = course.ar_name \
        if user.language == 'ar' \
        else course.en_name
    course_name = course_name if course_name else course.ar_name

    assignments = session.query(Assignment)\
        .filter(Assignment.course_id == course_id, Assignment.published==True)\
        .order_by(Assignment.assignment_number).all()

    keyboard = []

    for row_index in range(0, math.ceil(len(assignments) / 3)):
        row = []
        is_row_full = len(assignments) // 3 >= row_index + 1
        row_size = 3 if is_row_full else len(assignments) % 3
        row_start = row_index * 3

        for assignment_index in range(row_start, row_start + row_size):
            assignment = assignments[assignment_index]
            row.append(InlineKeyboardButton(
                f"{language['assignment']} {assignment.assignment_number}".capitalize(),
                callback_data=f'{ASSIGNMENT} {assignment.id}'),
            )

        if user.language == 'ar':
            row.reverse()

        keyboard.append(row)


    keyboard.append([
        back_to_course_button(language, user.language, course.en_name, course.ar_name, course.id),
    ])

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(
        text=f"{course_name}: {language['assignments'].capitalize()}",
        reply_markup=reply_markup
    )
    return STAGE_THREE



def list_course_exams(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)
    language = get_user_language(context.chat_data['language'])

    course_id, _ = query.data.split(' ')

    course = session.query(Course).filter(Course.id==course_id).one()

    exams = session.query(Exam).filter(Exam.course_id==course_id)\
        .order_by(Exam.date.desc()).all()

    course_name = course.ar_name \
        if user.language == 'ar' \
        else course.en_name
    course_name = course_name if course_name else course.ar_name

    keyboard = []

    for exam in exams:
        keyboard.append([
            InlineKeyboardButton(f'{exam.name}', callback_data=f'{EXAM} {exam.id}')
        ])

    keyboard.append([
        back_to_course_button(language, user.language, course.en_name, course.ar_name, course.id),
    ])

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(
        text=f"{course_name}: {language['exams'].capitalize()}",
        reply_markup=reply_markup
    )
    return STAGE_THREE