from flaskr.bot.utils.get_user_language import get_user_language
from flaskr.bot.utils.user_required import user_required
from flaskr.models import Lab, User
from flaskr import db
from telegram.ext import  CallbackContext
from telegram import  Update




def send_all_lab_files(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)
    user = session.query(User).filter(User.id==user.id).one()

    language = get_user_language(context.chat_data['language'])

    _, lab_id = query.data.split(' ')

    lab = session.query(Lab).filter(Lab.id==lab_id).one()

    course_name = lab.course.ar_name \
        if user.language == 'ar' \
        else lab.course.en_name

    query.message.reply_text(
        f"- {course_name}: {language['lab'].capitalize()} {lab.lab_number}"
    )

    for doc in lab.documents:
        query.bot.sendDocument(query.message.chat.id, document=doc.file_id)
        user.download_count += 1

    for vid in lab.videos:
        query.bot.sendVideo(query.message.chat.id, video=vid.file_id, caption=vid.file_name)
        user.download_count += 1

    for link in lab.youtube_links:
        query.bot.sendMessage(query.message.chat.id, text=link.url)
        user.download_count += 1
        
    session.commit()
    session.close()
    return None
