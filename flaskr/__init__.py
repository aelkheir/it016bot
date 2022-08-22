import signal
import os
from queue import Queue
import sys  
from threading import Thread
from flask import Flask, request
from sqlalchemy import MetaData
from flask_migrate import Migrate

import http

from telegram import Bot, Update
from telegram.ext import Dispatcher, PicklePersistence, Updater, JobQueue, CommandHandler
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

if app.env == 'development':
    from dotenv import load_dotenv
    load_dotenv()

PROD_SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
DEV_SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'

DATABASE_URI = PROD_SQLALCHEMY_DATABASE_URI \
    if app.env == 'production'\
    else DEV_SQLALCHEMY_DATABASE_URI 

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

metadata = MetaData(
    naming_convention={
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
})

db = SQLAlchemy(app, metadata=metadata)

with app.app_context():
    db.create_all()

migrate = Migrate(app, db, render_as_batch=True, compare_type=True)


from flaskr.bot.persistence import PostgresPersistence
from flaskr.bot.admin.admin_conv import admin_conv
from flaskr.bot.user.user_conv import user_conv
from flaskr.bot.owner.owner_conv import owner_conv
from flaskr.bot.notifications.notifications_conv import notifications_conv
from flaskr.bot.setlanguage import language_conv
from flaskr.bot.subscription import subscription_conv
from flaskr.bot.inlinequery.inline_conv import inline_conv
from flaskr.bot.user.handlers.start import start
from flaskr.bot.user.handlers.archive import list_semesters
from .bot.notifications.handle_notifications import handle_notifications


if app.env == 'production':

    BOT_TOKEN = os.getenv('BOT_TOKEN')
    bot = Bot(token=BOT_TOKEN)

    persistence = PostgresPersistence(store_bot_data=False)

    update_queue = Queue()
    job_queue = JobQueue()

    dispatcher = Dispatcher(
        bot=bot,
        persistence=persistence,
        update_queue=update_queue,
        job_queue=job_queue
    )

    job_queue.set_dispatcher(dispatcher)

    dispatcher.add_handler(inline_conv, )

    dispatcher.add_handler(CommandHandler(['courses', 'start'], start))
    dispatcher.add_handler(CommandHandler('archive', list_semesters))
    dispatcher.add_handler(CommandHandler('notifications', handle_notifications))
    dispatcher.add_handler(user_conv, )

    dispatcher.add_handler(admin_conv, 1)
    dispatcher.add_handler(owner_conv, 2)
    dispatcher.add_handler(language_conv, 3)
    dispatcher.add_handler(notifications_conv, 4)
    # dispatcher.add_handler(subscription_conv, 5)


    @app.route("/", methods=["POST", "GET"])
    def index():
        dispatcher.process_update(
            Update.de_json(request.get_json(force=True), bot))

        return "", http.HTTPStatus.NO_CONTENT


elif app.env == 'development':

    DEV_BOT_TOKEN = os.getenv('DEV_BOT_TOKEN')

    persistence = PostgresPersistence(store_bot_data=False)

    updater = Updater(
     token=DEV_BOT_TOKEN,
     persistence=persistence,
     use_context=True
    )

    dispatcher = updater.dispatcher

    dispatcher.add_handler(inline_conv, )

    dispatcher.add_handler(CommandHandler(['courses', 'start'], start))
    dispatcher.add_handler(CommandHandler('archive', list_semesters))
    dispatcher.add_handler(CommandHandler('notifications', handle_notifications))
    dispatcher.add_handler(user_conv, 1)

    dispatcher.add_handler(notifications_conv, 2)
    dispatcher.add_handler(admin_conv, 3)
    dispatcher.add_handler(owner_conv, 4)
    dispatcher.add_handler(language_conv, 5)
    # dispatcher.add_handler(subscription_conv, 6)

    @app.route("/")
    def dev():
        updater.start_polling()
        return ''
