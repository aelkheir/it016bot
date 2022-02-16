from flaskr.bot.utils.user_required import user_required
from flaskr.models import   Course, Lab, Lecture, User
from flaskr import db
from telegram.ext import  CallbackContext
from telegram import   Update



def send_lecture(update: Update, context: CallbackContext) -> int:
    session = db.session

    user = user_required(update, context, session)
    user = session.query(User).filter(User.id==user.id).one()

    user.start_count += 1

    language = context.chat_data['language']

    _, lecture_id = context.args[0].split('-')

    lecture = session.query(Lecture).filter(Lecture.id==lecture_id).one()

    course_name = lecture.course.ar_name \
        if user.language == 'ar' \
        else lecture.course.en_name

    update.message.reply_text(
        f"- {course_name.title()}: {language['lecture'].capitalize()} {lecture.lecture_number}"
    )

    for doc in lecture.documents:
        update.message.bot.sendDocument(update.message.chat_id, document=doc.file_id)
        user.download_count += 1

    for vid in lecture.videos:
        update.message.bot.sendVideo(update.message.chat_id, video=vid.file_id)
        user.download_count += 1

    for link in lecture.youtube_links:
        update.message.bot.sendMessage(update.message.chat_id, text=link.url)
        user.download_count += 1
        
    session.commit()
    session.close()
    return None


def send_lab(update: Update, context: CallbackContext) -> int:
    session = db.session

    user = user_required(update, context, session)
    user = session.query(User).filter(User.id==user.id).one()

    user.start_count += 1

    language = context.chat_data['language']

    _, lab_id = context.args[0].split('-')

    lab = session.query(Lab).filter(Lab.id==lab_id).one()

    course_name = lab.course.ar_name \
        if user.language == 'ar' \
        else lab.course.en_name

    update.message.reply_text(
        f"- {course_name.title()}: {language['lab'].capitalize()} {lab.lab_number}"
    )

    for doc in lab.documents:
        update.message.bot.sendDocument(update.message.chat_id, document=doc.file_id)
        user.download_count += 1

    for vid in lab.videos:
        update.message.bot.sendVideo(update.message.chat_id, video=vid.file_id)
        user.download_count += 1

    for link in lab.youtube_links:
        update.message.bot.sendMessage(update.message.chat_id, text=link.url)
        user.download_count += 1
        
    session.commit()
    session.close()
    return None


def send_references(update: Update, context: CallbackContext) -> int:
    session = db.session

    user = user_required(update, context, session)
    user = session.query(User).filter(User.id==user.id).one()

    user.start_count += 1

    language = context.chat_data['language']

    _, course_id = context.args[0].split('-')

    course = session.query(Course).filter(Course.id==course_id).one()

    course_name = course.ar_name \
        if user.language == 'ar' \
        else course.en_name

    update.message.reply_text(
        f"- {course_name.title()}: {language['references'].capitalize()}"
    )

    for reference in course.refferences:
        update.message.bot.sendDocument(update.message.chat_id, document=reference.file_id)
        user.download_count += 1

        
    session.commit()
    session.close()
    return None
