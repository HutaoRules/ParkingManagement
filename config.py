import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_DATABASE_URI =  'sqlite:///mydatabase.db'  #changeto ur url
    SQLALCHEMY_TRACK_MODIFICATIONS = False