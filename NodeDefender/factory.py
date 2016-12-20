import logging
from flask import Flask
from celery import Celery

def CreateApp():
    app = Flask(__name__)
    app.config.from_object('config')
    app.template_folder = "frontend/templates"
    app.static_folder = "frontend/static"
    return app

def CreateLogging():
    handler = logging.FileHandler('app.log')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger, handler

def CreateCelery(app):
    celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    return celery
