from flaskr.bot.utils.is_owner import is_owner
from flaskr.bot.owner.handlers.choice import  list_users
from flaskr import db
from telegram.ext import CallbackContext, CallbackContext
from telegram import Update
from flaskr.models import User



def delete_user(update: Update, context: CallbackContext) -> int:

    session = db.session
    
    if not is_owner(update, context, session):
        return

    # read from context
    user_id = context.chat_data['viewed_user_id']

    user = session.query(User).filter(User.id==user_id).one_or_none()

    if user:
        session.delete(user)
        update.message.reply_text(f'تم حذف المستخدم {user.first_name} {user.last_name if user.last_name else ""}')
    else:
        update.message.reply_text(f'حدث خطا: لم يتم العثور على {user.first_name}')



    session.commit()
    session.close()
    return list_users(update, context)
