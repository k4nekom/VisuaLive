import json
from logging import getLogger, config
from pathlib import Path

import responder

def create_app():
    BASE_DIR = Path(__file__).resolve().parents[1]

    api = responder.API(
        static_dir=str(BASE_DIR.joinpath('static')),
    )

    return api

def create_logger():
    with open('config/logging.json', 'r') as f:
        log_conf = json.load(f)

    config.dictConfig(log_conf)

    logger = getLogger('development')

    return logger

api = create_app()
logger = create_logger()