import NodeDefender
import os

default_config = {'syslog' : False,
                  'level' : 'DEBUG',
                  'filepath' : 'nodedefender.log',
                  'host' : '',
                  'port' : '514'}

config = default_config.copy()

def load_config(parser):
    if eval(parser['LOGGING']['SYSLOG']):
        config['syslog']=True
        config['host']=parser['LOGGING']['HOST']
        config['port']=parser['LOGGING']['PORT']
    NodeDefender.app.config.update(
        LOGGING_LEVEL=config['level'],
        LOGGING_SYSLOG=config['syslog'],
        LOGGING_FILEPATH=os.path.join(NodeDefender.config.datafolder,
            config['filepath']),
        LOGGING_HOST=config['host'],
        LOGGING_PORT=config['port'])
    return True

def set_default():
    config = default_config.copy()
    return True

def set(**kwargs):
    for key, value in kwargs.items():
        if key not in config:
            continue
        if key == "filepath":
            value = os.path.join(NodeDefender.config.datafolder, value)
        config[key] = str(value)
    return True

def write():
    NodeDefender.config.parser['LOGGING'] = config
    NodeDefender.config.write()
    return True
