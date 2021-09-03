from flaskr.bot.utils.user_required import user_required
from flaskr.models import  Course, Document, Exam, Lecture, Refference,  Video, YoutubeLink
from flaskr import db
from telegram.ext import  CallbackContext
from telegram import  Update



def send_lecture_file(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)

    _, file_id = query.data.split(' ')

    doc = session.query(Document).filter(Document.id==file_id).one_or_none()
    vid = session.query(Video).filter(Video.id==file_id).one_or_none()
    link = session.query(YoutubeLink).filter(YoutubeLink.id==file_id).one_or_none()

    if doc:
        query.bot.sendDocument(query.message.chat.id, document=doc.file_id)
        user.download_count += 1

    elif vid:
        query.bot.sendVideo(query.message.chat.id, video=vid.file_id)
        user.download_count += 1

    elif link:
        query.bot.sendMessage(query.message.chat.id, text=link.url)
        user.download_count += 1
        
    session.commit()
    session.close()
    return None

def send_all_lecture_files(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)
    language = context.chat_data['language']

    _, lecture_id = query.data.split(' ')

    lecture = session.query(Lecture).filter(Lecture.id==lecture_id).one()

    course_name = lecture.course.ar_name \
        if user.language == 'ar' \
        else lecture.course.en_name

    query.message.reply_text(
        f"- {course_name.title()}: {language['lecture'].capitalize()} {lecture.lecture_number}"
    )

    for doc in lecture.documents:
        query.bot.sendDocument(query.message.chat.id, document=doc.file_id)
        user.download_count += 1

    for vid in lecture.videos:
        query.bot.sendVideo(query.message.chat.id, video=vid.file_id)
        user.download_count += 1

    for link in lecture.youtube_links:
        query.bot.sendMessage(query.message.chat.id, text=link.url)
        user.download_count += 1
        
    session.commit()
    session.close()
    return None

def send_course_refference(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)

    _, refference_id = query.data.split(' ')

    refference = session.query(Refference).filter(Refference.id==refference_id).one()

    query.bot.sendDocument(query.message.chat.id, document=refference.file_id)
    user.download_count += 1

        
    session.commit()
    session.close()
    return None

def send_all_course_refferences(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)
    language = context.chat_data['language']

    _, course_id = query.data.split(' ')

    course = session.query(Course).filter(Course.id==course_id).one()

    course_name = course.ar_name \
        if user.language == 'ar' \
        else course.en_name
    course_name = course_name if course_name else course.ar_name

    if len(course.refferences) > 0:
        query.message.reply_text(
        f"{course_name.title()}: {language['references'].capitalize()}",
        )
        for refference in course.refferences:
            query.bot.sendDocument(query.message.chat.id, document=refference.file_id)
            user.download_count += 1

    session.commit()
    session.close()
    return None

def send_course_exam(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)

    _, exam_id = query.data.split(' ')

    exam = session.query(Exam).filter(Exam.id==exam_id).one()

    if exam.file_type == 'document':
        query.bot.sendDocument(query.message.chat.id, document=exam.file_id)
        user.download_count += 1

    elif exam.file_type == 'photo':
        query.bot.sendPhoto(query.message.chat.id, photo=exam.file_id)
        user.download_count += 1

        
    session.commit()
    session.close()
    return None

def send_all_course_exams(update: Update, context: CallbackContext) -> int:
    session = db.session

    query = update.callback_query
    query.answer()

    user = user_required(update, context, session)
    language = context.chat_data['language']

    _, course_id = query.data.split(' ')

    course = session.query(Course).filter(Course.id==course_id).one()

    course_name = course.ar_name \
        if user.language == 'ar' \
        else course.en_name
    course_name = course_name if course_name else course.ar_name

    if len(course.exams) > 0:

        query.message.reply_text(
            f"{course_name.title()}: {language['exams'].capitalize()}",
        )

        for exam in course.exams:
            if exam.file_type == 'document':
                query.message.reply_text(f'{exam.file_name}')
                query.bot.sendDocument(query.message.chat.id, document=exam.file_id)
                user.download_count += 1

            elif exam.file_type == 'photo':
                query.message.reply_text(f'{exam.file_name}')
                query.bot.sendPhoto(query.message.chat.id, photo=exam.file_id)
                user.download_count += 1

    session.commit()
    session.close()
    return None
