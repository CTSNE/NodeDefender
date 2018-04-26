import NodeDefender
import NodeDefender.config.celery 
import NodeDefender.config.database
import NodeDefender.config.general
import NodeDefender.config.logging
import NodeDefender.config.mail
import NodeDefender.config.redis
import configparser
import os

deployed = False
configfile = None

parser = configparser.ConfigParser()
basepath = os.path.abspath(os.path.dirname('..'))
datafolder = None

if os.path.exists(basepath + "/manage.py"):
    datafolder = basepath
else:
    datafolder = os.path.expanduser("~") + "/.nodedefender"
    if not os.path.isdir(datafolder):
        print("Creating folder: {}".format(datafolder))
        os.makedirs(datafolder)

configfile = datafolder + "/NodeDefender.conf"
migrations_folder = datafolder + "/sql_migrations"

def write_default():
    NodeDefender.config.celery.set_default()
    NodeDefender.config.database.set_default()
    NodeDefender.config.general.set_default()
    NodeDefender.config.logging.set_default()
    NodeDefender.config.mail.set_default()
    NodeDefender.config.redis.set_default()
    return write()

def load(fname = None):
    if os.path.exists(configfile):
        parser.read(configfile)
    else:
        return False

    global deployed
    deployed = True

    NodeDefender.config.celery.load_config(parser)
    NodeDefender.config.database.load_config(parser)
    NodeDefender.config.general.load_config(parser)
    NodeDefender.config.logging.load_config(parser)
    NodeDefender.config.mail.load_config(parser)
    NodeDefender.config.redis.load_config(parser)
    return True

def write():
    with open(configfile, 'w') as fw:
        parser.write(fw)
