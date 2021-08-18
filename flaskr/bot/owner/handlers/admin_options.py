from flaskr.bot.utils.is_owner import is_owner
from flaskr.bot.owner.handlers.choice import list_admins
from flaskr import db
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update
from flaskr.models import User



def delete_admin(update: Update, context: CallbackContext) -> int:

    session = db.session

    if not is_owner(update, context, session):
        return

    # read from context
    admin_id = context.chat_data['viewed_user_id']

    admin = session.query(User).filter(User.id==admin_id).one_or_none()

    if admin:
        admin.is_admin = False
        update.message.reply_text(f'تم حذف الادمن {admin.first_name} {admin.last_name if admin.last_name else ""}')
    else:
        update.message.reply_text(f'حدث خطا: لم يتم العثور على {admin.first_name}')



    session.commit()
    session.close()
    return list_admins(update, context)

