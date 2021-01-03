import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Thesecretkey'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{basedir}/footApp/database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
