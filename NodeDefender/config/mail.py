import NodeDefender

default_config = {'enabled' : False,
                  'host' : '',
                  'port' : 465,
                  'tls' : False,
                  'ssl' : False,
                  'username' : '',
                  'password' : ''}

config = default_config.copy()

def load_config(parser):
    if eval(parser['MAIL']['ENABLED']):
        config.update(parser['MAIL'])
        config['tls'] = eval(config['tls'])
        config['ssl'] = eval(config['ssl'])
    NodeDefender.app.config.update(
        MAIL = config['enabled'],
        MAIL_HOST=config['host'],
        MAIL_PORT=config['port'],
        MAIL_TLS=config['tls'],
        MAIL_SSL=config['ssl'],
        MAIL_USERNAME=config['username'],
        MAIL_PASSWORD=config['password'])
    return True

def set_default():
    config = default_config.copy()
    return True

def set(**kwargs):
    for key, value in kwargs.items():
        if key not in config:
            continue
        NodeDefender.config.mail.config[key] = str(value)
    return True

def write():
    NodeDefender.config.parser['MAIL'] = config
    return NodeDefender.config.write()
