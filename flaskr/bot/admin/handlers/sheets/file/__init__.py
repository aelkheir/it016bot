from flaskr.bot.utils.is_admin import is_admin
from flaskr.bot.admin.handlers.courses.course import list_refferences, list_sheets
from flaskr import db
from flaskr.models import  Course, Refference, Sheet
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update



def delete_file(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return

    # read from to context
    file_name = context.chat_data['file_name']

    sheet = session.query(Sheet).filter(Sheet.name==file_name).one()
    session.delete(sheet)
    update.message.reply_text(f'تم حذف {file_name}')    

    # refference = None
    # for ref in course.refferences:
    #     if ref.name == file_name:
    #         refference = ref
    #         break
    
    # if refference:
    #     session.delete(refference)
    #     update.message.reply_text(f'تم حذف {file_name}')

    # if not refference:
    #     update.message.reply_text(f'حدث خطا: لا يوجد {file_name}')
    

    # delete from to context
    del context.chat_data['file_name']

    session.commit()
    session.close()
    return list_sheets(update, context)

def send_sheet(update: Update, context: CallbackContext) -> int:
    session = db.session

    if not is_admin(update, context, session):
        return
    
    file_name = context.chat_data["file_name"]

    sheet: Sheet = session.query(Sheet).filter(Sheet.name==file_name).one()

    update.message.bot.send_document(
        update.message.chat_id,
        sheet.file_id
    )















    # # read from to context
    # course_id = context.chat_data['course_id']
    # file_name = context.chat_data['file_name']

    # files = session.query(Refference).join(Course)\
    #     .filter(Refference.name==file_name)\
    #     .filter(Course.id==course_id)\
    #     .all()
    # file = files[0]

    # update.message.bot.sendDocument(update.message.chat_id, document=file.file_id)
