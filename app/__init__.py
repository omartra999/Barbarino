from flask import Flask
from flask_pymongo import PyMongo
from config import Config
from dotenv import load_dotenv
import os

load_dotenv()

mongo = PyMongo()

app = Flask(__name__)
app.config.from_object(Config)

mongo.init_app(app)

#model imports

from app import models, routes, forms