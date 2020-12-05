from pathlib import Path

import responder

def create_app():
    BASE_DIR = Path(__file__).resolve().parents[1]

    api = responder.API(
        static_dir=str(BASE_DIR.joinpath('static')),
    )

    return api

def create_logger():
    from logging import getLogger, config

    config.dictConfig({
        'version': 1,
        'formatters': {
            'customFormatter': {
                'format': '%(asctime)s %(levelname)s - %(filename)s %(funcName)s %(lineno)d: %(message)s',
                'datefmt': '%Y/%m/%d %H:%M:%S'
            },
        },
        'handlers': {
            'developmentHandler': {
                'formatter': 'customFormatter',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'level': 'DEBUG',
                'filename': 'log/development.log',
                'encoding': 'utf8',
                'when': 'D',
                'interval': 1,
                'backupCount': 5
            },
            'consoleHandler': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'customFormatter'
            }
        },
        'root': {
            'handlers': [],
            'level': 'INFO'
        },
        'loggers': {
            'development': {
                'handlers': ['developmentHandler', 'consoleHandler'],
                'level': 'DEBUG',
                'propagate': 0
            }
        },
        'disable_existing_loggers': False
    })

    logger = getLogger('development')

    return logger

api = create_app()
logger = create_logger()