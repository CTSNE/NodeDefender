import NodeDefender.mqtt.message
import NodeDefender.mqtt.command
from NodeDefender.mqtt import connection

logger = None

def load():
    global logger
    logger = NodeDefender.logger.getChild("MQTT")
    mqttlist = NodeDefender.db.mqtt.list()
    if len(mqttlist) is 0:
        logger.warning("No MQTT Connection present")
        return True

    for mqtt in mqttlist: 
        connection.load(mqtt)
    logger.debug("MQTT Loaded")
    return True
