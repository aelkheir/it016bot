import re
from typing import Match
from uuid import uuid4

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, ParseMode, InputTextMessageContent
from telegram.ext import  CallbackContext
from telegram.utils.helpers import escape_markdown, create_deep_linked_url

from flaskr import db
from flaskr.bot.localization.en import en
from flaskr.bot.localization.ar import ar
from flaskr.bot.user.user_constants import ASSIGNMENT, EXAM, LAB, LECTURE, REFFERENCES, TUTORIAL
from flaskr.bot.utils.get_current_semester import get_current_semester
from flaskr.models import Assignment, Course, Lab, Lecture,  Semester, Tutorial


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
        results.extend(get_tutorials(course, context, 'keyboard'))
        results.extend(get_references(course, context, 'keyboard'))
        results.extend(get_assignments(course, context, 'keyboard'))
        results.extend(get_exams(course, context, 'keyboard'))
    
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
        results.extend(get_tutorials(course, context, 'keyboard'))
        results.extend(get_references(course, context, 'keyboard'))
        results.extend(get_assignments(course, context, 'keyboard'))
        results.extend(get_exams(course, context, 'keyboard'))
    
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
        results.extend(get_tutorials(course, context, match.string, mode='text'))
        results.extend(get_references(course, context, match.string, mode='text'))
        results.extend(get_assignments(course, context, match.string, mode='text'))
        results.extend(get_exams(course, context, match.string, mode='text'))
    
    return results



def get_lectures(
  course,
  context: CallbackContext,
  message: str =None,
  mode='keyboard'
  ):
    session = db.session()
    results = []

    course_name = course.en_name 

    if len(course_name.split(' ')) > 2:
      course_name = ' '.join(course_name.split(' ')[0:2]) + '..'

    lectures = session.query(Lecture) \
      .filter(Lecture.course_id==course.id) \
      .order_by(Lecture.id).all()

    for lecture in lectures:
      files_lenght = len(lecture.documents) + len(lecture.videos)

      url =  create_deep_linked_url(context.bot.username, f'{LECTURE}-{lecture.id}')

      if mode == 'keyboard':

        keyboard = []

        keyboard.append([
            InlineKeyboardButton(
              f'{files_lenght} {"files" if files_lenght > 1 else "file"}'.title(),
              url=url,
              ),
        ])

        reply_markup = InlineKeyboardMarkup(keyboard)

      # incase mode == 'keyboard'
      title = f'{course_name}: {en["lecture"].title()} {lecture.lecture_number}'
      description = f'{files_lenght} {"files" if files_lenght > 1 else "file"}'
      text = f'''*{escape_markdown(
              f'{course.en_name}: {en["lecture"].title()} {lecture.lecture_number}'
            )}*'''

      # incase mode == 'text'
      if mode == 'text' and message:
        title = f'Insert links into message'
        description = f'{course_name} {en["lecture"]} {lecture.lecture_number}'
        text = f'''[{escape_markdown(
                description
              )}]({url})'''
        text = insert_regex.sub(text, message)

      results.append(
        InlineQueryResultArticle(
            id=str(uuid4()),
            title=title.title(),
            description=description,
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
    session = db.session()
    results = []

    course_name = course.en_name 

    labs = session.query(Lab) \
      .filter(Lab.course_id==course.id) \
      .order_by(Lab.id).all()

    if len(course_name.split(' ')) > 2:
      course_name = ' '.join(course_name.split(' ')[0:2]) + '..'

    for lab in labs:
      files_lenght = len(lab.documents) + len(lab.videos)

      url =  create_deep_linked_url(context.bot.username, f'{LAB}-{lab.id}')

      if mode == 'keyboard':
        keyboard = []

        keyboard.append([
            InlineKeyboardButton(
              f'{files_lenght} {"files" if files_lenght > 1 else "file"}'.title(),
              url=url,
              ),
        ])

        reply_markup = InlineKeyboardMarkup(keyboard)

      # incase mode == 'keyboard'
      title = f'{course_name}: {en["lab"].title()} {lab.lab_number}'
      description = f'{files_lenght} {"files" if files_lenght > 1 else "file"}'
      text = f'''*{escape_markdown(
               title
             )}*'''

      # incase mode == 'text'
      if mode == 'text' and message:
        title = f'Insert links into message'
        description = f'{course_name} {en["lab"]} {lab.lab_number}'
        text = f'''[{escape_markdown(
                description
              )}]({url})'''
        text = insert_regex.sub(text, message)


      results.append(
        InlineQueryResultArticle(
            id=str(uuid4()),
            title=title.title(),
            description=description,
            input_message_content=InputTextMessageContent(
              text,
              parse_mode=ParseMode.MARKDOWN,
              disable_web_page_preview=True,
            ),
            reply_markup= reply_markup if mode == 'keyboard' else None
        ),
      )

    return results

def get_tutorials(
  course,
  context: CallbackContext,
  message: str =None,
  mode='keyboard'
  ):
    session = db.session()
    results = []

    course_name = course.en_name 

    if len(course_name.split(' ')) > 2:
      course_name = ' '.join(course_name.split(' ')[0:2]) + '..'

    tutorials = session.query(Tutorial) \
      .filter(Tutorial.course_id==course.id) \
      .order_by(Tutorial.id).all()

    for tutorial in tutorials:
      files_lenght = len(tutorial.documents) + len(tutorial.videos)

      url =  create_deep_linked_url(context.bot.username, f'{TUTORIAL}-{tutorial.id}')

      if mode == 'keyboard':
        keyboard = []

        keyboard.append([
            InlineKeyboardButton(
              f'{files_lenght} {"files" if files_lenght > 1 else "file"}'.title(),
              url=url,
              ),
        ])

        reply_markup = InlineKeyboardMarkup(keyboard)

      # incase mode == 'keyboard'
      title = f'{course_name}: {en["tutorial"].title()} {tutorial.tutorial_number}'
      description = f'{files_lenght} {"files" if files_lenght > 1 else "file"}'
      text = f'''*{escape_markdown(
               title
             )}*'''

      # incase mode == 'text'
      if mode == 'text' and message:
        title = f'Insert links into message'
        description = f'{course_name} {en["tutorial"]} {tutorial.tutorial_number}'
        text = f'''[{escape_markdown(
                description
              )}]({url})'''
        text = insert_regex.sub(text, message)


      results.append(
        InlineQueryResultArticle(
            id=str(uuid4()),
            title=title.title(),
            description=description,
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

    course_name = course.en_name 

    if len(course_name.split(' ')) > 2:
      course_name = ' '.join(course_name.split(' ')[0:2]) + '..'

    if course.refferences:


      files_lenght = len(course.refferences)

      url =  create_deep_linked_url(context.bot.username, f'{REFFERENCES}-{course.id}')

      if mode == 'keyboard':
        keyboard = []

        keyboard.append([
            InlineKeyboardButton(
              f'{files_lenght} {"files" if files_lenght > 1 else "file"}'.title(),
              url=url,
              ),
        ])

        reply_markup = InlineKeyboardMarkup(keyboard)


      # incase mode == 'keyboard'
      title = f'{course_name}: {en["references"].title()}'
      description = f'{files_lenght} {"files" if files_lenght > 1 else "file"}'
      text = f'''*{escape_markdown(
               title
             )}*'''

      # incase mode == 'text'
      if mode == 'text' and message:
        title = f'Insert links into message'
        description = f'{course_name} {en["references"]}'
        text = f'''[{escape_markdown(
                description
              )}]({url})'''
        text = insert_regex.sub(text, message)

      results.append(
        InlineQueryResultArticle(
            id=str(uuid4()),
            title=title.title(),
            description=description,
            input_message_content=InputTextMessageContent(
              text,
              parse_mode=ParseMode.MARKDOWN,
              disable_web_page_preview=True,
            ),
            reply_markup=reply_markup if mode == 'keyboard' else None
        ),
      )

    return results

def get_assignments(
  course,
  context: CallbackContext,
  message: str =None,
  mode='keyboard'
  ):
    session = db.session()
    results = []

    course_name = course.en_name 

    if len(course_name.split(' ')) > 2:
      course_name = ' '.join(course_name.split(' ')[0:2]) + '..'

    assignments = session.query(Assignment) \
      .filter(Assignment.course_id==course.id) \
      .order_by(Assignment.id).all()


    for assignment in assignments:

      files_lenght = len(assignment.documents)
      files_lenght = files_lenght if files_lenght else len(assignment.photos)

      url =  create_deep_linked_url(context.bot.username, f'{ASSIGNMENT}-{assignment.id}')

      type_of_files = ''
      if len(assignment.documents):
        type_of_files = 'files'
      else:
        type_of_files = 'pages'
      type_of_files = type_of_files[:] if files_lenght > 1 else type_of_files[:-1]

      if mode == 'keyboard':
        keyboard = []
        keyboard.append([
            InlineKeyboardButton(
              f'{files_lenght} {type_of_files}'.title(),
              url=url,
              ),
        ])

        reply_markup = InlineKeyboardMarkup(keyboard)


      # incase mode == 'keyboard'
      title = f'{course_name}: {en["assignment"].title()} {assignment.assignment_number}'
      description = f'{files_lenght} {type_of_files}'
      text = f'''*{escape_markdown(
               title
             )}*'''

      # incase mode == 'text'
      if mode == 'text' and message:
        title = f'Insert links into message'
        description = f'{course_name} {en["assignment"]} {assignment.assignment_number}'
        text = f'''[{escape_markdown(
                description
              )}]({url})'''
        text = insert_regex.sub(text, message)

      results.append(
        InlineQueryResultArticle(
            id=str(uuid4()),
            title=title.title(),
            description=description,
            input_message_content=InputTextMessageContent(
              text,
              parse_mode=ParseMode.MARKDOWN,
              disable_web_page_preview=True,
            ),
            reply_markup=reply_markup if mode == 'keyboard' else None
        ),
      )

    return results

def get_exams(
  course,
  context: CallbackContext,
  message: str =None,
  mode='keyboard'
  ):
    results = []

    course_name = course.en_name 

    if len(course_name.split(' ')) > 2:
      course_name = ' '.join(course_name.split(' ')[0:2]) + '..'

    for exam in course.exams:

      files_lenght = len(exam.documents)
      files_lenght = files_lenght if files_lenght else len(exam.photos)

      url =  create_deep_linked_url(context.bot.username, f'{EXAM}-{exam.id}')

      type_of_files = ''
      if len(exam.documents):
        type_of_files = 'files'
      else:
        type_of_files = 'pages'
      type_of_files = type_of_files[:] if files_lenght > 1 else type_of_files[:-1]

      if mode == 'keyboard':
        keyboard = []
        keyboard.append([
            InlineKeyboardButton(
              f'{files_lenght} {type_of_files}'.title(),
              url=url,
              ),
        ])

        reply_markup = InlineKeyboardMarkup(keyboard)


      # incase mode == 'keyboard'
      title = f'{course_name}: {exam.name}'
      description = f'{files_lenght} {type_of_files}'
      text = f'''*{escape_markdown(
               title
             )}*'''

      # incase mode == 'text'
      if mode == 'text' and message:
        title = f'Insert links into message'
        description = f'{exam.name} {course_name}'
        text = f'''[{escape_markdown(
                description
              )}]({url})'''
        text = insert_regex.sub(text, message)

      results.append(
        InlineQueryResultArticle(
            id=str(uuid4()),
            title=title.title(),
            description=description,
            input_message_content=InputTextMessageContent(
              text,
              parse_mode=ParseMode.MARKDOWN,
              disable_web_page_preview=True,
            ),
            reply_markup=reply_markup if mode == 'keyboard' else None
        ),
      )

    return results
