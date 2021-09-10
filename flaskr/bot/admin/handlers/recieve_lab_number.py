from flaskr.bot.admin.handlers.labs_list import list_lab_files
from flaskr.bot.utils.is_admin import is_admin
from flaskr.bot.admin.admin_constants import RECIEVE_LAB_NUMBER
import re
from flaskr import db
from flaskr.models import  Lab
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update 



def recieve_lab_number(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    # reads from context
    lab_id = context.chat_data['lab_id']

    number_regex = re.compile(f'\d+')
    number_match = number_regex.search(update.message.text)

    if number_match:
        lab = session.query(Lab).filter(Lab.id==lab_id).one()
        lab.lab_number = number_match.group()
        session.commit()
        session.close()
        return list_lab_files(update, context, lab_id=lab_id)

    else:
        update.message.reply_text(f'''الرجاء ادخال رقم اللاب مباشرة، مثال:
        3''' )
        return RECIEVE_LAB_NUMBER
