from redis import ConnectionPool, StrictRedis
from functools import wraps
import random
import NodeDefender

logger = None
conn = None

class LocalStorage:
    def __init__(self):
        self.h = {}
        self.s = {}

    def hmset(self, key, values):
        for k, v in values.items():
            try:
                self.h[key][k] = str(v)
            except KeyError:
                self.h[key] = {}
                self.h[key][k] = str(v)
        return self.h[key]

    def hset(self, key, k, value):
        try:
            self.h[key][k] = str(value)
        except KeyError:
            self.h[key] = {}
            self.h[key][k] = str(value)
        return self.h[key][k]

    def hget(self, key, k):
        try:
            return self.h[key][k]
        except KeyError:
            return None

    def hgetall(self, key):
        try:
            return self.h[key]
        except KeyError:
            return {}

    def hkeys(self, key):
        try:
            return set(self.h[key])
        except KeyError:
            return set()

    def hdel(self, key, *values):
        for value in values:
            try:
                self.h[key].pop(value)
            except KeyError:
                pass
        return True

    def sadd(self, key, value):
        try:
            self.s[key].add(value)
        except KeyError:
            self.s[key] = set()
            self.s[key].add(value)
        return self.s[key]

    def smembers(self, key):
        try:
            return self.s[key]
        except KeyError:
            return set()

    def srandmember(self, key, items = 1):
        try:
            random.sample(self.s[key], items)
        except KeyError:
            return None

    def srem(self, key, value):
        try:
            self.s[key].remove(value)
        except KeyError:
            return False
        return self.s[key]

def load(loggHandler):
    global conn
    global logger
    logger = NodeDefender.db.logger.getChild("Redis")
    if NodeDefender.config.redis.config['enabled']:
        host = NodeDefender.config.redis.config['host']
        port = NodeDefender.config.redis.config['port']
        db = NodeDefender.config.redis.config['database']
        pool = ConnectionPool(host=host, port=int(port), db=db, decode_responses=True)
        conn = StrictRedis(connection_pool=pool)
    else:
        NodeDefender.db.redis.logger.\
                warning("Local Storage, application data is only during run- time")
        conn = LocalStorage()
    NodeDefender.db.redis.logger.info("Local Storage caching initialized")

def redisconn(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, conn = conn, **kwargs)
    return wrapper

from NodeDefender.db.redis import icpe, sensor, field, mqtt
