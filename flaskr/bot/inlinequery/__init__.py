import re
from uuid import uuid4

from telegram import InlineQueryResultArticle, InlineQueryResultCachedDocument, ParseMode, InputTextMessageContent, Update
from telegram.ext import  CallbackContext
from telegram.utils.helpers import escape_markdown

from flaskr import db
from flaskr.bot.inlinequery.constants import SEND
from flaskr.bot.inlinequery.search import get_all_courses, get_course, insert_link
from flaskr.models import Document

insert_link_regex = re.compile(r'.*(\+(.*)\+).*')


def inlinequery(update: Update, context: CallbackContext) -> None:
    session = db.session

    query = update.inline_query.query

    insert_link_match = insert_link_regex.match(query)

    results = []

    if query == '':
      results = get_all_courses(session, context)

    if insert_link_match:
      results = insert_link(session, context, insert_link_match)

    else:

      results = get_course(session, context, query)

    update.inline_query.answer(
      results,
      auto_pagination=True,
      switch_pm_text='📖 Courses',
      switch_pm_parameter='start'
      )

    session.close()