import flaskr.bot.inlinequery.constants as constants
from uuid import uuid4

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, ParseMode, InputTextMessageContent
from telegram.ext import  CallbackContext
from telegram.utils.helpers import escape_markdown, create_deep_linked_url

from flaskr import db
from flaskr.bot.inlinequery.constants import LAB, LECTURE, REFERENCES
from flaskr.bot.localization.en import en
from flaskr.bot.utils.get_current_semester import get_current_semester
from flaskr.models import Course, Document, Semester


def get_all_courses(session, context: CallbackContext) -> None:
    session = db.session

    current_semester = get_current_semester(session)


    courses =  session.query(Course) \
        .join(Semester, Semester.id == Course.semester_id) \
        .filter((Semester.id==current_semester.semester_id )) \
        .order_by(Course.en_name).all()

    results = []


    for course in courses:
        results.extend(get_lectures(course, context))
        results.extend(get_labs(course, context))
        results.extend(get_references(course, context))
    
    return results


def get_course(session, context: CallbackContext, query: str) -> None:
    session = db.session

    current_semester = get_current_semester(session)

    courses =  session.query(Course) \
        .join(Semester, Semester.id == Course.semester_id) \
        .filter((Semester.id==current_semester.semester_id )) \
        .filter((Course.en_name.ilike(f'%{query}%')) | (Course.ar_name.like(f'%{query}%'))) \
        .order_by(Course.en_name).all()

    results = []


    for course in courses:
        results.extend(get_lectures(course, context))
        results.extend(get_labs(course, context))
        results.extend(get_references(course, context))
    
    return results



def get_lectures(course, context: CallbackContext):
    results = []

    course_name = course.en_name if course.en_name else course.ar_name

    if len(course_name.split(' ')) > 2:
      course_name = ' '.join(course_name.split(' ')[0:3]) + '...'


    for lecture in course.lectures:

      keyboard = []

      files_lenght = len(lecture.documents) + len(lecture.videos)

      url =  create_deep_linked_url(context.bot.username, f'{LECTURE}-{lecture.id}')

      keyboard.append([
          InlineKeyboardButton(
            f'get {files_lenght} {"files" if files_lenght > 1 else "file"}'.title(),
            url=url,
            ),
      ])

      reply_markup = InlineKeyboardMarkup(keyboard)

      results.append(
        InlineQueryResultArticle(
            id=str(uuid4()),
            title=f'{course_name} -> {en["lecture"].title()} {lecture.lecture_number}',
            description=f'{files_lenght} {"files" if files_lenght > 1 else "file"}'.title(),
            input_message_content=InputTextMessageContent(
                f'''*{escape_markdown(
                  f'{course.en_name} -> {en["lecture"].title()} {lecture.lecture_number}'
                )}*''',
                parse_mode=ParseMode.MARKDOWN
            ),
            reply_markup=reply_markup
        ),
      )

    return results

def get_labs(course, context: CallbackContext):
    results = []

    course_name = course.en_name if course.en_name else course.ar_name

    if len(course_name.split(' ')) > 2:
      course_name = ' '.join(course_name.split(' ')[0:3]) + '...'

    for lab in course.labs:

      keyboard = []

      files_lenght = len(lab.documents) + len(lab.videos)

      url =  create_deep_linked_url(context.bot.username, f'{LAB}-{lab.id}')

      keyboard.append([
          InlineKeyboardButton(
            f'get {files_lenght} {"files" if files_lenght > 1 else "file"}'.title(),
            url=url,
            ),
      ])

      reply_markup = InlineKeyboardMarkup(keyboard)

      results.append(
        InlineQueryResultArticle(
            id=str(uuid4()),
            title=f'{course_name} -> {en["lab"].title()} {lab.lab_number}',
            description=f'{files_lenght} {"files" if files_lenght > 1 else "file"}'.title(),
            input_message_content=InputTextMessageContent(
                f'''*{escape_markdown(
                  f'{course.en_name} -> {en["lab"].title()} {lab.lab_number}'
                )}*''',
                parse_mode=ParseMode.MARKDOWN
            ),
            reply_markup=reply_markup
        ),
      )

    return results


def get_references(course, context: CallbackContext):
    results = []

    course_name = course.en_name if course.en_name else course.ar_name

    if len(course_name.split(' ')) > 2:
      course_name = ' '.join(course_name.split(' ')[0:3]) + '...'

    if course.refferences:

      keyboard = []

      files_lenght = len(course.refferences)

      url =  create_deep_linked_url(context.bot.username, f'{REFERENCES}-{course.id}')

      keyboard.append([
          InlineKeyboardButton(
            f'get {files_lenght} {"files" if files_lenght > 1 else "file"}'.title(),
            url=url,
            ),
      ])

      reply_markup = InlineKeyboardMarkup(keyboard)

      results.append(
        InlineQueryResultArticle(
            id=str(uuid4()),
            title=f'{course_name} -> {en["references"].title()}',
            description=f'{files_lenght} {"files" if files_lenght > 1 else "file"}'.title(),
            input_message_content=InputTextMessageContent(
                f'''*{escape_markdown(
                  f'{course.en_name} -> {en["references"].title()}'
                )}*''',
                parse_mode=ParseMode.MARKDOWN
            ),
            reply_markup=reply_markup
        ),
      )

    return results
