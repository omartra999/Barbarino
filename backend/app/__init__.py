from flask import Flask
from mongoengine import connect
from config import Config
from dotenv import load_dotenv
from flask_mail import Mail, Message
import os
import yagmail



load_dotenv()

app = Flask(__name__)


mail = Mail(app)
app.config.from_object(Config)

yag = yagmail.SMTP(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
connect(host= app.config['MONGO_URI'])

#model imports
from app import models, routes, forms