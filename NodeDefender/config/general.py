from datetime import datetime
import NodeDefender

default_config = {'run_mode' : 'TESTING',
                  'key' : 'key',
                  'salt' : 'salt',
                  'port' : '5000',
                  'self_registration' : True}

config = default_config.copy()

def load_config(parser):
    config.update(parser['GENERAL'])
    config['port'] = int(config['port'])
    config['self_registration'] = eval(config['self_registration'])
    NodeDefender.app.config.update(
        RUN_MODE=config['run_mode'],
        SECRET_KEY=config['key'],
        SECRET_SALT=config['salt'])

    if config['run_mode'].upper() == 'DEVELOPMENT':
        NodeDefender.app.config.update(DEBUG=True)
    elif config['run_mode'].upper() == 'TESTING':
        NodeDefender.app.config.update(
            DEBUG=True,
            TESTING=True)
    return True

def uptime():
    return str(datetime.now() - NodeDefender.DATE_LOADED)

def set_default():
    config = default_config.copy()
    return True

def set(**kwargs):
    for key, value in kwargs.items():
        if key not in config:
            continue
        NodeDefender.config.general.config[key] = str(value)
    return True

def write():
    config['deployed'] = True
    NodeDefender.config.parser['GENERAL'] = config
    return NodeDefender.config.write()
