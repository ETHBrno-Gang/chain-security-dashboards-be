import os
import logging


logger = logging.getLogger(__name__)


class Config:
    SECRET_KEY = os.environ["SECRET_KEY"]

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_ECHO = True for sqlalchemy logging all queries
    DATABASE_PARAMETERS = os.getenv("DATABASE_PARAMETERS", "")
    if os.getenv("SQLALCHEMY_DATABASE_URI") is None:
        logger.error('Please provide the database uri with the SQLALCHEMY_DATABASE_URI environment variable')
        raise RuntimeError('No SQLALCHEMY_DATABASE_URI configured')
    # Heroku adds a postgres:// env variable. But SQLAlchemy accepts only postgresql://
    SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"].replace("postgres://", "postgresql://", 1) + DATABASE_PARAMETERS

    SESSION_TYPE = "sqlalchemy"
