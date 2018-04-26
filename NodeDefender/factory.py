import logging
from flask import Flask
from flask_moment import Moment
from celery import Celery
from itsdangerous import URLSafeSerializer
from flask_wtf.csrf import CSRFProtect
import os
import sys
import NodeDefender

csfr = CSRFProtect()
moment = Moment()

def CreateApp():
    app = Flask(__name__)
    mode = NodeDefender.config.general.config['run_mode']
    app.config.from_object('NodeDefender.config.factory.DefaultConfig')
    app.template_folder = "templates"
    app.static_folder = "templates/frontend/static"
    moment.init_app(app)
    return app

def CreateLogging(app = None):
    app = app or CreateApp()
    
    logger = logging.getLogger("NodeDefender")
    logger.setLevel(logging.DEBUG)
    
    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    level = NodeDefender.config.logging.config['level']
    level = level if len(level) else 'debug'

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel('WARNING')
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)
    if not NodeDefender.config.deployed:
        return logger, console_handler
    file_handler = logging.FileHandler(app.config['LOGGING_FILEPATH'])
    file_handler.setLevel(level)
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    if app.config['LOGGING_SYSLOG']:
        syslog_handler = logging.handlers.\
            SysLogHandler(address = (app.config['LOGGING_HOST'],
                                     int(app.config['LOGGING_PORT'])))
        syslog_handler.setLevel(level)
        logger.addHandler(syslog_handler)
    return logger, console_handler

def CreateCelery(app = None):
    app = app or CreateApp()
    if not NodeDefender.config.celery.config['enabled']:
        NodeDefender.logger.info("Concurrency disabled")
        return False

    try:
        celery = Celery(app.name, broker=app.config['CELERY_BROKER_URI'],
                   backend=app.config['CELERY_BACKEND_URI'])
    except KeyError:
        celery = Celery(app.name)
        NodeDefender.logger.info("Concurreny configuration error")
        return False
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    NodeDefender.logger.info("Concurrency successfully enabled")
    return celery

class Serializer:
    def __init__(self, app):
        self.serializer = URLSafeSerializer(app.config['SECRET_KEY'])
        self.salt = app.config['SECRET_SALT']

    def loads(self, token):
        return self.serializer.loads(token)

    def dumps(self, string):
        return self.serializer.dumps(string)

    def loads_salted(self, token):
        return self.serializer.loads(token, salt=self.salt)

    def dumps_salted(self, string):
        return self.serializer.dumps(string, salt=self.salt)
