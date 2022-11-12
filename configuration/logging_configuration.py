import logging
import logging.config
import logging.handlers
import os

logger = logging.getLogger(__name__)
DEFAULT_LOG_LEVEL = os.getenv('PROJECT_LOG_LEVEL', '') or ('DEBUG' if os.getenv('FLASK_ENV', '') == 'development' else 'INFO')


def get_project_log_level():
    project_log_level = os.getenv('PROJECT_LOG_LEVEL', DEFAULT_LOG_LEVEL)
    available_log_levels = list(logging._nameToLevel.keys())
    if project_log_level not in available_log_levels:
        logging.warning(f'The specified logging level "{project_log_level}" is not recognised.'
                        f' Available levels are: {available_log_levels}')
        project_log_level = DEFAULT_LOG_LEVEL
    return project_log_level


def configure_logging():
    project_log_level = get_project_log_level()
    logging.warning(f'Project log level is set to {project_log_level}')

    logger_configuration_dict = {
        'version': 1,

        'formatters': {
            'default_fmt': {
                'format': '%(process)d | %(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
            'small_fmt': {
                'format': '[%(levelname)s] %(name)s: %(message)s'
            },
        },

        'handlers': {
            'default': {
                'level': project_log_level,
                'formatter': 'small_fmt',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
            }
        },

        'loggers': {
            '': {
                'handlers': ['default'],
                'level': project_log_level,
                'propagate': True
             },
            'src': {
                'handlers': ['default'],
                'level': logging.DEBUG,
                'propagate': False
             },
            'sqlalchemy.engine.Engine': {
                'level': logging.WARNING,
                'propagate': True
            },
            'sqlalchemy.engine': {
                'level': logging.WARNING,
                'propagate': True
            },
            'urllib3.connectionpool': {
                'level': logging.WARNING,
            },
            'three_commas.streams': {
                'level': logging.DEBUG,
                'propagate': True
            },
            'gunicorn.error': {
                'level': logging.DEBUG,
            }
        }
    }

    logging.config.dictConfig(logger_configuration_dict)

