import NodeDefender
import NodeDefender.icpe.sensor.command
import NodeDefender.icpe.sensor.commandclass

logger = None

def load(loggHandler, *icpes):
    global logger
    logger = NodeDefender.icpe.logger.getChild("sensor")
    for icpe in icpes:
        for sensor in icpe.sensors:
            NodeDefender.db.sensor.get(icpe.mac_address, sensor.sensor_id)
            NodeDefender.mqtt.command.sensor.\
                    sensor_info(icpe.mac_address, sensor.sensor_id)
            logger.debug("Sensor {}:{} Loaded".\
                         format(icpe.mac_address, sensor.sensor_id))
            NodeDefender.db.field.load_from_sensor(sensor)
    return True

def verify_list(icpe, *sensors):
    known = [sensor.sensor_id for sensor in NodeDefender.db.sensor.list(icpe)]

    for sensor in sensors:
        if sensor not in known:
            NodeDefender.db.sensor.create(icpe, sensor)

    for sensor in known:
        if sensor not in sensors:
            NodeDefender.db.sensor.delete(icpe, sensor)
    return True

def sensor_info(icpe, sensor_id, **payload):
    sensor = NodeDefender.db.sensor.get_sql(icpe, sensor_id)
    
    sensor.sleepable = bool(eval(payload['sleepable']))
    sensor.wakeup_interval = payload['wakeup_interval']

    info = NodeDefender.icpe.zwave.devices.info(payload['vid'], payload['pid'])
    if info:
        sensor.vendor_id = payload['vid']
        sensor.product_id = payload['pid']
        sensor.product_type = info['ProductTypeId'].strip()
        sensor.vendor_name = info['Brand'].strip()
        sensor.product_name = info['Name'].strip()
        sensor.device_type = info['DeviceType'].strip()
        sensor.library_type = info['LibraryType'].strip()
    else:
        sensor.vendor_id = payload['vid']
        sensor.product_id = payload['pid']
        sensor.product_type = "Undefined"
        sensor.vendor_name = "Undefined"
        sensor.product_name = "Undefined"
        sensor.device_type = "Undefined"
        sensor.library_type = "Undefined"
        NodeDefender.icpe.logger.\
                warning("Unable to find Z-Wave- data for {}:{}. On {}".\
                       format(payload['vid'], payload['pid'], icpe))

    NodeDefender.icpe.sensor.commandclass.\
            commandclasses(icpe, sensor_id, *payload['clslist_0'].split(','))
    NodeDefender.db.sensor.save_sql(sensor)
    NodeDefender.db.redis.sensor.load(sensor)
    return NodeDefender.db.sensor.get(icpe, sensor_id)

def event(mac_address, sensor_id, command_class, **payload):
    if command_class == 'info':
        return True
    try:
        data = NodeDefender.icpe.zwave.event(mac_address, sensor_id, \
                                         command_class, **payload)
    except AttributeError:
        NodeDefender.icpe.logger.warning("Got unsuported Command Class:{!s}"\
                                        .format(command_class))
        return False

    if not data:
        return False
    
    commandclass = data['commandclass']['name']
    if data['commandclasstype']:
        commandclasstype = data['commandclasstype']['name']
    else:
        commandclasstype = None
    
    NodeDefender.frontend.sockets.zwave.event(mac_address, sensor_id, data)
    NodeDefender.db.field.update(mac_address, sensor_id, data['fields']['name'],\
                                 **{'value' : data['value'], 'state' : data['state']})
    
    if data['fields']['type'] == 'bool':
        NodeDefender.db.data.sensor.event.put(mac_address, sensor_id,\
                                       commandclass, commandclasstype,\
                                       data['state'], data['value'])
    if data['fields']['name'] == 'Watt':
        NodeDefender.db.data.sensor.power.put(mac_address, sensor_id,
                                              data['value'])
    elif data['fields']['name'] == 'Celsius':
        NodeDefender.db.data.sensor.heat.put(mac_address, sensor_id,
                                             data['value'])
    return True
