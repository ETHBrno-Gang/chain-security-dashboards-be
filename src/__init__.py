from configuration import configure_project
configure_project()
from configuration import flask_config

import logging # noqa
from flask_sqlalchemy import SQLAlchemy # noqa
from flask import Flask # noqa


logger = logging.getLogger(__name__)


def create_app():
    _app = Flask(__name__)
    _app.config.from_object(flask_config.Config)
    return _app


app = create_app()

# Database
db = SQLAlchemy(app)

from .persistence import models # noqa
app.app_context().push()
db.create_all()
db.engine.dispose()  # needs to after db.create_all()


from . import api
API_V1_PREFIX = '/api/v1'
app.register_blueprint(api.v1.naka.blueprint, url_prefix=API_V1_PREFIX)

logger.info('App has loaded and is running')

#idea
#progress
# pitch
# demo

#memes and zksync