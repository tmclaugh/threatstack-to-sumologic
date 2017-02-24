#!/usr/bin/env python

from app import create_app
import app.models.sumologic as sumologic_model
import logging
from logging.config import fileConfig
import os

fileConfig('logging.conf', disable_existing_loggers=False)
if os.environ.get('TS_DEBUG'):
    logging.root.setLevel(level=logging.DEBUG)
_logger = logging.getLogger(__name__)

# Gunicorn entry point.
application = create_app()

if __name__ == '__main__':
    # Entry point when run via Python interpreter.
    _logger.debug('== Running in debug mode ==')
    _logger.info('== Checking collector and source existance ==')
    sl = sumologic_model.SumoLogicModel()
    if not sl.check_collector_exists():
        _logger.info('== Creating Sumo Logic Collector ==')
        collector = sl.create_collector()

    if not sl.check_source_exists():
        _logger.info('== Creating Sumo Logic Source ==')
        source = sl.create_source()

    application.run(host='localhost', port=8080, debug=True)
