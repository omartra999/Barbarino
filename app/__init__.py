from flask import Flask
from mongoengine import connect
from config import Config
from dotenv import load_dotenv
import os

load_dotenv()

mongo = PyMongo()

app = Flask(__name__)
app.config.from_object(Config)

connect(host= app.Config['MONGO_URI'])

#model imports

from app import models, routes, forms