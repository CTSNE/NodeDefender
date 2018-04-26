from NodeDefender.db.sql import SQL, iCPEModel, NodeModel
import NodeDefender
from NodeDefender.db import redis
from redlock import RedLock
from datetime import datetime

def get_sql(mac_address):
    return SQL.session.query(iCPEModel).\
            filter(iCPEModel.mac_address == mac_address).first()

def update_sql(mac_address, **kwargs):
    icpe = get_sql(mac_address)
    if icpe is None:
        return False

    try:
        for key, value in kwargs.items():
            if key not in icpe.columns():
                continue
            setattr(icpe, key, value)
    except ValueError:
        return False

    SQL.session.add(icpe)
    SQL.session.commit()
    return icpe

def create_sql(mac_address, mqttsrc):
    if get_sql(mac_address):
        return False
    mqtt = NodeDefender.db.mqtt.get_sql(**mqttsrc)
    icpe = iCPEModel(mac_address)
    mqtt.icpes.append(icpe)
    SQL.session.add(mqtt, icpe)
    SQL.session.commit()
    NodeDefender.db.logger.info("Created SQL Entry for {!r}".format(mac_address))
    return icpe

def delete_sql(mac_address):
    icpe = get_sql(mac_address)
    if icpe is None:
        return False
    SQL.session.delete(icpe)
    NodeDefender.db.logger.info("Deleted SQL Entry for {!r}".format(mac_address))
    return SQL.session.commit()

def get_redis(mac_address):
    return redis.icpe.get(mac_address)

def update_redis(mac_address, **kwargs):
    return redis.icpe.save(mac_address, **kwargs)

def delete_redis(mac_address):
    return redis.icpe.flush(mac_address)

def get(mac_address):
    icpe = get_redis(mac_address)
    if len(icpe):
        return icpe
    if redis.icpe.load(get_sql(mac_address)):
        NodeDefender.db.logger.debug('Loaded iCPE: {!r}'.format(mac_address))
        return get_redis(mac_address)
    return False

def create(mac_address, mqttsrc):
    if not create_sql(mac_address, mqttsrc):
        return False
    NodeDefender.mqtt.command.icpe.zwave_info(mac_address)
    NodeDefender.mqtt.command.icpe.system_info(mac_address)
    NodeDefender.db.message.icpe_created(get_sql(mac_address))
    return get(mac_address)

def update(mac_address, **data):
    update_sql(mac_address, **data)
    return update_redis(mac_address, **data)

def delete(mac_address):
    for sensor in NodeDefender.db.sensor.list(mac_address):
        NodeDefender.db.sensor.delete(mac_address, sensor.sensor_id)
        
    delete_sql(mac_address)
    delete_redis(mac_address)
    return True

def list(node = None):
    if node:
        return SQL.session.query(iCPEModel).join(iCPEModel.node).\
                filter(NodeModel.name == node).all()
    return SQL.session.query(iCPEModel).all()

def unassigned(user):
    return SQL.session.query(iCPEModel).\
            filter(iCPEModel.node == None).all()

def sensors(mac_address):
    sensors = redis.sensor.list(mac_address)
    if len(sensors):
        return sensors
    if load_redis(mac_address):
        return redis.sensor.list(mac_address)
    return False

def update_state(mac_address, state):
    icpe = get(mac_address)
    if not icpe:
        return False
    icpe['state'] = state
    websocket.icpe.state(mac_address, state)
    update_redis(icpe)
    return True

def online(mac_address):
    icpe = get(mac_address)
    if not icpe:
        return False
    return eval(icpe['online'])

def mark_online(mac_address):
    icpe = get(mac_address)
    if not icpe:
        return False
    if eval(icpe['online']):
        return icpe
    NodeDefender.db.logger.info("iCPE {} Online".format(mac_address))
    NodeDefender.frontend.sockets.icpe.online(icpe)
    return update_redis(mac_address, online = True)

def mark_offline(mac_address):
    icpe = get(mac_address)
    if not icpe:
        return False
    if not eval(icpe['online']):
        return icpe
    NodeDefender.db.logger.warning("iCPE {} Offline".format(mac_address))
    NodeDefender.frontend.sockets.icpe.offline(icpe)
    return update_redis(mac_address, online = False)

def connection(mac_address):
    icpe = get(mac_address)
    if not icpe:
        return False
    return {'ipAddress' : icpe['ipAddress']}

def power(mac_address):
    icpe = get(mac_address)
    if not icpe:
        return False
    return {'power' : icpe['power']}
