import logging
from dotenv import load_dotenv
from .logging_configuration import configure_logging


logger = logging.getLogger(__name__)


def configure_project():
    load_dotenv()
    configure_logging()
