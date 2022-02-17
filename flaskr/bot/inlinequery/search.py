import re
from typing import Match
from uuid import uuid4

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, ParseMode, InputTextMessageContent
from telegram.ext import  CallbackContext
from telegram.utils.helpers import escape_markdown, create_deep_linked_url

from flaskr import db
from flaskr.bot.inlinequery.constants import LAB, LECTURE, REFERENCES
from flaskr.bot.localization.en import en
from flaskr.bot.localization.ar import ar
from flaskr.bot.utils.get_current_semester import get_current_semester
from flaskr.models import Course,  Semester


def get_all_courses(session, context: CallbackContext) -> None:
    session = db.session

    current_semester = get_current_semester(session)


    courses =  session.query(Course) \
        .join(Semester, Semester.id == Course.semester_id) \
        .filter((Semester.id==current_semester.semester_id )) \
        .order_by(Course.en_name).all()

    results = []


    for course in courses:
        results.extend(get_lectures(course, context, 'keyboard'))
        results.extend(get_labs(course, context, 'keyboard'))
        results.extend(get_references(course, context, 'keyboard'))
    
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
        results.extend(get_lectures(course, context, 'keyboard'))
        results.extend(get_labs(course, context, 'keyboard'))
        results.extend(get_references(course, context, 'keyboard'))
    
    return results


insert_regex = re.compile(r'\+.*\+', re.DOTALL)


def insert_link(session, context: CallbackContext, match: Match[str]) -> None:
    session = db.session

    current_semester = get_current_semester(session)

    course_name = match.groups()[1]

    courses =  session.query(Course) \
        .join(Semester, Semester.id == Course.semester_id) \
        .filter((Semester.id==current_semester.semester_id )) \
        .filter((Course.en_name.ilike(f'%{course_name}%')) | (Course.ar_name.like(f'%{course_name}%'))) \
        .order_by(Course.en_name).all()

    results = []


    for course in courses:
        results.extend(get_lectures(course, context, match.string, mode='text'))
        results.extend(get_labs(course, context, match.string, mode='text'))
        results.extend(get_references(course, context, match.string, mode='text'))
    
    return results



def get_lectures(
  course,
  context: CallbackContext,
  message: str =None,
  mode='keyboard'
  ):
    results = []

    course_name = course.en_name if mode == 'keyboard' else course.ar_name

    if len(course_name.split(' ')) > 2:
      course_name = ' '.join(course_name.split(' ')[0:2]) + '...'

    for lecture in course.lectures:
      files_lenght = len(lecture.documents) + len(lecture.videos)

      url =  create_deep_linked_url(context.bot.username, f'{LECTURE}-{lecture.id}')

      if mode == 'keyboard':

        keyboard = []

        keyboard.append([
            InlineKeyboardButton(
              f'get {files_lenght} {"files" if files_lenght > 1 else "file"}'.title(),
              url=url,
              ),
        ])

        reply_markup = InlineKeyboardMarkup(keyboard)

      # incase mode == 'keyboard'
      title = f'{course_name} -> {en["lecture"].title()} {lecture.lecture_number}'
      description = f'{files_lenght} {"files" if files_lenght > 1 else "file"}'
      text = f'''*{escape_markdown(
              f'{course.en_name} -> {en["lecture"].title()} {lecture.lecture_number}'
            )}*'''

      # incase mode == 'text'
      if mode == 'text' and message:
        title = f'Insert links into message'
        description = f'{ar["lecture"]} {lecture.lecture_number} {course_name}'
        text = f'''[{escape_markdown(
                description
              )}]({url})'''
        text = insert_regex.sub(text, message)

      results.append(
        InlineQueryResultArticle(
            id=str(uuid4()),
            title=title.title(),
            description=description.title(),
            input_message_content=InputTextMessageContent(
              text,
              parse_mode=ParseMode.MARKDOWN,
              disable_web_page_preview=True,
            ),
            reply_markup=reply_markup if mode == 'keyboard' else None
        ),
      )

    return results

def get_labs(
  course,
  context: CallbackContext,
  message: str =None,
  mode='keyboard'
  ):
    results = []

    course_name = course.en_name if mode == 'keyboard' else course.ar_name

    if len(course_name.split(' ')) > 2:
      course_name = ' '.join(course_name.split(' ')[0:2]) + '...'

    for lab in course.labs:


      files_lenght = len(lab.documents) + len(lab.videos)

      url =  create_deep_linked_url(context.bot.username, f'{LAB}-{lab.id}')

      if mode == 'keyboard':
        keyboard = []

        keyboard.append([
            InlineKeyboardButton(
              f'get {files_lenght} {"files" if files_lenght > 1 else "file"}'.title(),
              url=url,
              ),
        ])

        reply_markup = InlineKeyboardMarkup(keyboard)

      # incase mode == 'keyboard'
      title = f'{course_name} -> {en["lab"].title()} {lab.lab_number}'
      description = f'{files_lenght} {"files" if files_lenght > 1 else "file"}'
      text = f'''*{escape_markdown(
               title
             )}*'''

      # incase mode == 'text'
      if mode == 'text' and message:
        title = f'Insert links into message'
        description = f'{ar["lab"]} {lab.lab_number} {course_name}'
        text = f'''[{escape_markdown(
                description
              )}]({url})'''
        text = insert_regex.sub(text, message)


      results.append(
        InlineQueryResultArticle(
            id=str(uuid4()),
            title=title.title(),
            description=description.title(),
            input_message_content=InputTextMessageContent(
              text,
              parse_mode=ParseMode.MARKDOWN,
              disable_web_page_preview=True,
            ),
            reply_markup= reply_markup if mode == 'keyboard' else None
        ),
      )

    return results


def get_references(
  course,
  context: CallbackContext,
  message: str =None,
  mode='keyboard'
  ):
    results = []

    course_name = course.en_name if mode == 'keyboard' else course.ar_name

    if len(course_name.split(' ')) > 2:
      course_name = ' '.join(course_name.split(' ')[0:2]) + '...'

    if course.refferences:


      files_lenght = len(course.refferences)

      url =  create_deep_linked_url(context.bot.username, f'{REFERENCES}-{course.id}')

      if mode == 'keyboard':
        keyboard = []

        keyboard.append([
            InlineKeyboardButton(
              f'get {files_lenght} {"files" if files_lenght > 1 else "file"}'.title(),
              url=url,
              ),
        ])

        reply_markup = InlineKeyboardMarkup(keyboard)


      # incase mode == 'keyboard'
      title = f'{course_name} -> {en["references"].title()}'
      description = f'{files_lenght} {"files" if files_lenght > 1 else "file"}'
      text = f'''*{escape_markdown(
               title
             )}*'''

      # incase mode == 'text'
      if mode == 'text' and message:
        title = f'Insert links into message'
        description = f'{ar["references"][2:]} {course_name}'
        text = f'''[{escape_markdown(
                description
              )}]({url})'''
        text = insert_regex.sub(text, message)


      results.append(
        InlineQueryResultArticle(
            id=str(uuid4()),
            title=title.title(),
            description=description.title(),
            input_message_content=InputTextMessageContent(
              text,
              parse_mode=ParseMode.MARKDOWN,
              disable_web_page_preview=True,
            ),
            reply_markup=reply_markup if mode == 'keyboard' else None
        ),
      )

    return results
