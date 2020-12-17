import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    with open('admin_info.txt', mode='r') as file:
        key = file.readline().rstrip()
    SECRET_KEY = os.environ.get('SECRET_KEY') or key

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
