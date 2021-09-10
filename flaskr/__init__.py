import os
from flask import Flask, request
from sqlalchemy import MetaData
from flask_migrate import Migrate

import http

from telegram import Bot, Update
from telegram.ext import Dispatcher, PicklePersistence, Updater
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

migrate = Migrate(app, db, render_as_batch=True)


from flaskr.bot.admin.admin_conv import admin_conv
from flaskr.bot.user.user_conv import user_conv
from flaskr.bot.owner.owner_conv import owner_conv
from flaskr.bot.setlanguage import language_conv

if app.env == 'production':

    BOT_TOKEN = os.getenv('BOT_TOKEN')
    bot = Bot(token=BOT_TOKEN)

    persistence = PicklePersistence(filename='pickle')

    dispatcher = Dispatcher(bot=bot, persistence=persistence, update_queue=None, workers=0)

    dispatcher.add_handler(user_conv, 1)
    dispatcher.add_handler(admin_conv, 2)
    dispatcher.add_handler(owner_conv, 3)
    dispatcher.add_handler(language_conv, 4)


    @app.route("/", methods=["POST", "GET"])
    def index():
        dispatcher.process_update(
            Update.de_json(request.get_json(force=True), bot))

        return "", http.HTTPStatus.NO_CONTENT


elif app.env == 'development':

    DEV_BOT_TOKEN = os.getenv('DEV_BOT_TOKEN')

    dev_persistence = PicklePersistence(filename='dev_pickle')

    updater = Updater(token=DEV_BOT_TOKEN, persistence=dev_persistence, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(user_conv, 1)
    dispatcher.add_handler(admin_conv, 2)
    dispatcher.add_handler(owner_conv, 3)
    dispatcher.add_handler(language_conv, 4)

    @app.route("/dev")
    def dev():
        updater.start_polling()
        return ''
