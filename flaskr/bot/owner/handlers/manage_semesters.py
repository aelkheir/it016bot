import math
from flaskr.bot.owner.owner_constants import SEMESTER_LIST
from flaskr.bot.utils.is_owner import is_owner
from flaskr import db
from flaskr.models import Course, Semester
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update, ReplyKeyboardMarkup
import logging
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup 
from flaskr.bot.admin.admin_constants import COURSE_LIST


def manage_semesters(update: Update, context: CallbackContext) -> int:

    user = update.message.from_user

    session = db.session

    if not is_owner(update, context, session):
        return

    if 'semester_id' in context.chat_data:
        del context.chat_data['semester_id']
    
    semesters =  session.query(Semester).order_by(Semester.number).all()

    reply_keyboard = []

    for row_index in range(0, math.ceil(len(semesters) / 2)):
        row = []
        is_row_full =  len(semesters) // 2 >= row_index + 1
        row_size = 2 if is_row_full else len(semesters) % 2
        row_start = row_index * 2

        for semester_index in range(row_start, row_start + row_size):
            semester = semesters[semester_index]
            row.append( f'سمستر {semester.number}')

        reply_keyboard.append(row)

    reply_keyboard.append(['اضافة سمستر'])

    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

    update.message.reply_text(
        f'السمسترات',
        reply_markup=markup,
    )

    session.close()
    return SEMESTER_LIST
