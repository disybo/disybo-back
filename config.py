import os

class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite://:memory:'

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI =  os.environ['DISYBO_URI']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
