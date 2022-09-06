import math
import re
from flaskr.bot.notifications.notifications_constants import NOTIFIED_LAB, NOTIFIED_TUTORIAL 
from flaskr.bot.utils.get_user_language import get_user_language
from flaskr.models import Lab, Tutorial
from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, constants
from flaskr import db


course_regex = re.compile(r'\+c\+')
number_regex = re.compile(r'\+n\+')

def tutorial_notification_message(update: Update, context: CallbackContext) -> int:
  session = db.session

  query = update.callback_query
  query.answer()

  chat_id = update.effective_chat.id

  user_language = context.chat_data['language']

  language = get_user_language(user_language)

  _, tutorial_id = query.data.split(' ')

  tutorial = session.query(Tutorial).filter(Tutorial.id==tutorial_id).one()
  course = tutorial.course

  keyboard = [
    [
        InlineKeyboardButton(f"{language['show'].capitalize()} {language['more']}",
        callback_data=f'{NOTIFIED_TUTORIAL} {tutorial_id}'),
    ]
  ]
  reply_markup = InlineKeyboardMarkup(keyboard)

  course_name = course.ar_name \
      if user_language == 'ar' \
      else course.en_name

  template = language['notify_tutorial_template']
  message = re.sub(course_regex, course_name, template)
  message = '🔔  ' + re.sub(number_regex, f'{tutorial.tutorial_number}', message)

  context.bot.edit_message_text(
      text=message,
      reply_markup=reply_markup,
      chat_id=chat_id,
      message_id=query.message.message_id,
      parse_mode=constants.PARSEMODE_MARKDOWN_V2
  )