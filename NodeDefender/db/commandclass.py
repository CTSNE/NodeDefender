from NodeDefender.db.sql import SQL, iCPEModel, SensorModel,\
                                CommandClassModel, CommandClassTypeModel
import NodeDefender

def get_sql(mac_address, sensor_id, classnumber = None, classname = None):
    if classnumber is None and classname is None:
        raise TypeError('Please enter either classnumber or classname')
    if classnumber:
        return SQL.session.query(CommandClassModel).\
                join(CommandClassModel.sensor).\
                join(SensorModel.icpe).\
                filter(iCPEModel.mac_address == mac_address).\
                filter(SensorModel.sensor_id == sensor_id).\
                filter(CommandClassModel.number == classnumber).first()
    elif classname:
        return SQL.session.query(CommandClassModel).\
                join(CommandClassModel.sensor).\
                join(SensorModel.icpe).\
                filter(iCPEModel.mac_address == mac_address).\
                filter(SensorModel.sensor_id == sensor_id).\
                filter(CommandClassModel.name == classname).first()

def update_sql(mac_address, sensor_id, classnumber = None, classname = None, **kwargs):
    if classnumber:
        commandclass = get_sql(mac_address, sensor_id, classnumber = classnumber)
    elif classname:
        commandclass = get_sql(mac_address, sensor_id, classname = classname)
    else:
        raise TypeError('Please enter either classnumber or classname')

    if commandclass is None:
        return False

    columns = commandclass.columns()
    for key, value in kwargs.items():
        if key not in columns:
            continue
        setattr(commandclass, key, value)

    SQL.session.add(commandclass)
    SQL.session.commit()
    return commandclass

def create_sql(mac_address, sensor_id, classnumber = None, classname = None):
    if classnumber:
        commandclass = get_sql(mac_address, sensor_id, classnumber = classnumber)
    elif classname:
        commandclass = get_sql(mac_address, sensor_id, classname = classname)
    else:
        raise TypeError('Please enter either classnumber or classname')
    
    if commandclass:
        return commandclass

    commandclass = CommandClassModel(classnumber, classname)
    sensor = NodeDefender.db.sensor.get_sql(mac_address, sensor_id)
    if sensor is None:
        return False
    sensor.commandclasses.append(commandclass)
    SQL.session.add(sensor, commandclass)
    SQL.session.commit()
    NodeDefender.db.logger.debug("Created SQL Entry for {!r}:{!r}:{!r}".\
                 format(mac_address, sensor_id, commandclass.number))
    return commandclass

def delete_sql(mac_address, sensor_id, classnumber = None, classname = None):
    if classnumber:
        commandclass = get_sql(mac_address, sensor_id, classnumber = classnumber)
    elif classname:
        commandclass = get_sql(mac_address, sensor_id, classname = classname)
    else:
        raise TypeError('Please enter either classnumber or classname')

    if commandclass is None:
        return False
    SQL.session.delete(commandclass)
    NodeDefender.db.logger.debug("Deleted SQL Entry for {!r}:{!r}:{!r}".\
                 format(mac_address, sensor_id, commandclass.number))
    return SQL.session.commit()

def get(mac_address, sensor_id, classnumber = None, classname = None):
    return get_sql(mac_address, sensor_id, classnumber = classnumber, \
                 classname = classname)

def update(mac_address, sensor_id, classnumber = None, classname = None, **kwargs):
    return update_sql(mac_address, sensor_id, classnumber = classnumber, \
                      classname = classname, **kwargs)

def update_nameless():
    commandclasses = CommandClassModel.query.filter_by(name = None).all()
    for commandclass in commandclasses:
        mac_address = commandclass.sensor.icpe.mac_address
        sensor_id = commandclass.sensor.sensor_id
        classnumber = commandclass.number
        info = NodeDefender.icpe.zwave.commandclass.info(classnumber=classnumber)
        if info:
            update(mac_address, sensor_id, classnumber=classnumber, **info)
            NodeDefender.db.logger.info("Updated Commandclass {}, for {}:{}".\
                                        format(info['name'], mac_address, sensor_id))
            if info['types']:
                NodeDefender.mqtt.command.commandclass.\
                        sup(mac_address, sensor_id, info['name'])
    return True


def list(mac_address, sensor_id):
    sensor = NodeDefender.db.sensor.get_sql(mac_address, sensor_id)
    if not sensor:
        return []
    return sensor.commandclasses

def number_list(mac_address, sensor_id):
    sensor = NodeDefender.db.sensor.get_sql(mac_address, sensor_id)
    if sensor:
        return [c.number for c in sensor.commandclasses]
    else:
        return []

def create(mac_address, sensor_id, classnumber):
    if not create_sql(mac_address, sensor_id, classnumber):
        return False
    info = NodeDefender.icpe.zwave.commandclass.info(classnumber = classnumber)
    if info:
        update(mac_address, sensor_id, classnumber = classnumber, **info)
        if info['types']:
            NodeDefender.mqtt.command.commandclass.sup(mac_address, sensor_id, \
                                                       info['name'])
    if NodeDefender.icpe.zwave.commandclass.\
       web_field(classnumber = classnumber):
        update(mac_address, sensor_id, classnumber = classnumber, **{'web_field' :
                                                                True})
    NodeDefender.db.field.load_commandclass(get_sql(mac_address, sensor_id,
                                                    classnumber = classnumber))
    return get(mac_address, sensor_id, classnumber = classnumber)

def update_zwave(mac_address, sensor_id, classnumber):
    if not get_sql(mac_address, sensor_id, classnumber = classnumber):
        return False
    info = NodeDefender.icpe.zwave.commandclass.info(classnumber = classnumber)
    if info:
        update(mac_address, sensor_id, classnumber = classnumber, **info)
        if info['types']:
            NodeDefender.mqtt.command.commandclass.sup(mac_address, sensor_id, \
                                                       info['name'])
    if NodeDefender.icpe.zwave.commandclass.\
       web_field(classnumber = classnumber):
        update(mac_address, sensor_id, classnumber = classnumber, **{'web_field' :
                                                                True})
    NodeDefender.db.field.load_commandclass(get_sql(mac_address, sensor_id,
                                                    classnumber = classnumber))
    return get(mac_address, sensor_id, classnumber = classnumber)


def delete(mac_address, sensor_id, classnumber = None, classname = None):
    return delete_sql(mac_address, sensor_id, classnumber = classnumber, \
                      classname = classname)

def add_type(mac_address, sensor_id, classname, classtype):
    commandclass = get_sql(mac_address, sensor_id, classname = classname)
    if commandclass is None:
        return False
    typeModel = CommandClassTypeModel(classtype)
    info = NodeDefender.icpe.zwave.commandclass.\
            info(classname = classname, classtype = classtype)
    web_field = NodeDefender.icpe.zwave.commandclass.\
            web_field(classname = classname, classtype = classtype)
    if not info:
        NodeDefender.db.logger.debug("Unsupported Commandclasstype {}:{}".\
                                     format(commandclass.name, classtype))
        return False
    typeModel.name = info['name']
    if web_field:
        typeModel.web_field = True
    commandclass.types.append(typeModel)
    SQL.session.add(commandclass, typeModel)
    SQL.session.commit()
    NodeDefender.db.field.load_commandclasstype(typeModel)
    return True

def get_type(mac, sensor_id, classname, classtype):
    return SQL.session.query(CommandClassTypeModel).\
            join(CommandClassTypeModel.commandclass).\
            join(CommandClassModel.sensor).\
            join(SensorModel.icpe).\
            filter(iCPEModel.mac_address == mac).\
            filter(SensorModel.sensor_id == sensor_id).\
            filter(CommandClassModel.name == classname).\
            filter(CommandClassTypeModel.name == classtype).first()
