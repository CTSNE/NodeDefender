import NodeDefender.db.sql
import NodeDefender.db.redis

logger = None

def load(app, loggHandler):
    global logger
    logger = NodeDefender.logger.getChild("database")
    NodeDefender.db.sql.load(app, loggHandler)
    NodeDefender.db.redis.load(loggHandler)

import NodeDefender.db.data
import NodeDefender.db.group
import NodeDefender.db.user
import NodeDefender.db.message
import NodeDefender.db.node
import NodeDefender.db.icpe
import NodeDefender.db.sensor
import NodeDefender.db.commandclass
import NodeDefender.db.field
import NodeDefender.db.mqtt
