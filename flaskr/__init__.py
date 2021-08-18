import os
from flask import Flask, request
import http

from telegram import Bot, Update
from telegram.ext import Dispatcher, PicklePersistence
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)



SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')


app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


from flaskr.bot.admin.admin_conv import admin_conv
from flaskr.bot.user.user_conv import user_conv
from flaskr.bot.owner.owner_conv import owner_conv

with app.app_context():
    db.create_all()

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