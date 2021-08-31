import os
from dotenv import load_dotenv
from flask import Flask, request
import http

from telegram import Bot, Update
from telegram.ext import Dispatcher, PicklePersistence, Updater
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

flask_env = os.getenv('FLASK_ENV')

app = Flask(__name__)

PROD_SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
DEV_SQLALCHEMY_DATABASE_URI = os.getenv('DEV_SQLALCHEMY_DATABASE_URI')

DATABASE_URI = PROD_SQLALCHEMY_DATABASE_URI \
    if flask_env == 'production'\
    else DEV_SQLALCHEMY_DATABASE_URI 

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from flaskr.bot.admin.admin_conv import admin_conv
from flaskr.bot.user.user_conv import user_conv
from flaskr.bot.owner.owner_conv import owner_conv

with app.app_context():
    db.create_all()


if flask_env == 'production':

    BOT_TOKEN = os.getenv('BOT_TOKEN')
    bot = Bot(token=BOT_TOKEN)

    persistence = PicklePersistence(filename='pickle')

    dispatcher = Dispatcher(bot=bot, persistence=persistence, update_queue=None, workers=0)
    dispatcher.add_handler(user_conv, 1)
    dispatcher.add_handler(admin_conv, 2)
    dispatcher.add_handler(owner_conv, 3)


    @app.route("/", methods=["POST", "GET"])
    def index():
        dispatcher.process_update(
            Update.de_json(request.get_json(force=True), bot))

        return "", http.HTTPStatus.NO_CONTENT


elif flask_env == 'development':

    DEV_BOT_TOKEN = os.getenv('DEV_BOT_TOKEN')

    dev_persistence = PicklePersistence(filename='dev_pickle')

    updater = Updater(token=DEV_BOT_TOKEN, persistence=dev_persistence, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(user_conv, 1)
    dispatcher.add_handler(admin_conv, 2)
    dispatcher.add_handler(owner_conv, 3)

    @app.route("/dev")
    def dev():
        updater.start_polling()
        return ''
