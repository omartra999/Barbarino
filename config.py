import os

class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/Barbarino')
    DEBUG = os.environ.get('DEBUG', 'False') == 'True'

    MAIL_SERVER = 'smtp.gmail.com'  
    MAIL_PORT = 465 
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')   
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')   
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT')