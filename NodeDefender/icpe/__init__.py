import NodeDefender

logger = None

def load(loggHandler):
    global logger
    logger = NodeDefender.logger.getChild("iCPE")
    icpes = NodeDefender.db.icpe.list()
    for icpe in icpes:
        if NodeDefender.db.icpe.online(icpe.mac_address):
            continue
        NodeDefender.db.icpe.get(icpe.mac_address)
        NodeDefender.mqtt.command.icpe.zwave_info(icpe.mac_address)
        NodeDefender.mqtt.command.icpe.system_info(icpe.mac_address)
        logger.debug("iCPE {} Loaded".format(icpe.mac_address))
    NodeDefender.icpe.sensor.load(loggHandler, *icpes)
    logger.info("iCPE Service Loaded")
    return True

from NodeDefender.icpe import zwave, system, sensor, event
