from uuid import uuid4

from telegram import InlineQueryResultArticle, InlineQueryResultCachedDocument, ParseMode, InputTextMessageContent, Update
from telegram.ext import  CallbackContext
from telegram.utils.helpers import escape_markdown

from flaskr import db
from flaskr.bot.inlinequery.constants import SEND
from flaskr.bot.inlinequery.search import get_all_courses, get_course
from flaskr.models import Document


def inlinequery(update: Update, context: CallbackContext) -> None:
    session = db.session

    query = update.inline_query.query

    results = []

    if query == '':
      results = get_all_courses(session, context)

    else:
      results = get_course(session, context, query)

    update.inline_query.answer(
      results,
      auto_pagination=True,
      cache_time=0,
      switch_pm_text='📖 Courses',
      switch_pm_parameter='start'
      )

    session.close()