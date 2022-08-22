import math
import re
from flaskr.bot.notifications.notifications_constants import LECTURE_NOTIFICATION_MESSAGE, NOTIFIED_LECTURE, NOTIFIED_LECTURE_OPTIONS
from flaskr.bot.utils.buttons import back_to_course_button
from flaskr.bot.utils.get_user_language import get_user_language
from flaskr.bot.utils.user_required import user_required
from flaskr.models import Lecture
from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, constants
from flaskr.bot.user.user_constants import  FILE, LECTURE, SHOW_GLOBAL_NOTE
from flaskr import db


course_regex = re.compile(r'\+c\+')
number_regex = re.compile(r'\+n\+')

def lecture_notification_message(update: Update, context: CallbackContext) -> int:
  session = db.session

  query = update.callback_query
  query.answer()

  chat_id = update.effective_chat.id

  user_language = context.chat_data['language']

  language = get_user_language(user_language)

  _, lecture_id = query.data.split(' ')

  lecture = session.query(Lecture).filter(Lecture.id==lecture_id).one()
  course = lecture.course

  keyboard = [
    [
          InlineKeyboardButton(f"{language['show'].capitalize()} {language['more']}",
          callback_data=f'{NOTIFIED_LECTURE} {lecture_id}'),
    ]
  ]
  reply_markup = InlineKeyboardMarkup(keyboard)

  course_name = course.ar_name \
      if user_language == 'ar' \
      else course.en_name

  template = language['notify_lecture_template']
  message = re.sub(course_regex, course_name, template)
  message = '🔔  ' + re.sub(number_regex, f'{lecture.lecture_number}', message)

  context.bot.edit_message_text(
      text=message,
      reply_markup=reply_markup,
      chat_id=chat_id,
      message_id=query.message.message_id,
      parse_mode=constants.PARSEMODE_MARKDOWN_V2
  )