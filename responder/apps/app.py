import os
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

api = create_app()

def set_logging():
    if os.environ['ENV'] == 'development':
        with open('config/logging.json', 'r') as f:
            log_conf = json.load(f)['development']
    elif os.environ['ENV'] =='test':
        with open('config/logging.json', 'r') as f:
            log_conf = json.load(f)['test']

    config.dictConfig(log_conf)

def make_logger():
    if os.environ['ENV'] == 'development':
        return getLogger('app.development')
    elif os.environ['ENV'] =='test':
        return getLogger('app.test')

logger = make_logger()