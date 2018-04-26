from NodeDefender.db.sql import SQL, iCPEModel, SensorModel
from NodeDefender.db import redis
import NodeDefender

def get_sql(mac_address, sensor_id):
    return SQL.session.query(SensorModel).join(SensorModel.icpe).\
            filter(iCPEModel.mac_address == mac_address).\
            filter(SensorModel.sensor_id == sensor_id).first()

def update_sql(mac_address, sensor_id, **kwargs):
    sensor = get_sql(mac_address, sensor_id)
    if sensor is None:
        return False

    columns = sensor.columns()
    for key, value in kwargs.items():
        if key not in columns:
            continue
        setattr(sensor, key, value)

    SQL.session.add(sensor)
    SQL.session.commit()
    return sensor

def save_sql(sensor):
    SQL.session.add(sensor)
    return SQL.session.commit()

def create_sql(mac_address, sensor_id):
    if get_sql(mac_address, sensor_id):
        return False

    icpe = NodeDefender.db.icpe.get_sql(mac_address)
    sensor = SensorModel(sensor_id)
    icpe.sensors.append(sensor)
    SQL.session.add(icpe, sensor)
    SQL.session.commit()
    NodeDefender.db.logger.info("Created SQL Entry for {!r}:{!r}".format(mac_address, sensor_id))
    return sensor

def delete_sql(mac_address, sensor_id):
    sensor = get_sql(mac_address, sensor_id)
    if sensor is None:
        return False
    SQL.session.delete(sensor)
    NodeDefender.db.logger.info("Deleted SQL Entry for {!r}:{!r}".format(mac_address, sensor_id))
    return SQL.session.commit()

def get_redis(mac_address, sensor_id):
    return redis.sensor.get(mac_address, sensor_id)

def update_redis(mac_address, sensor_id, **kwargs):
    return redis.sensor.save(mac_address, sensor_id, **kwargs)

def delete_redis(mac_address, sensor_id):
    return redis.sensor.flush(mac_address, sensor_id)

def get(mac_address, sensor_id):
    sensor = get_redis(mac_address, sensor_id)
    if len(sensor):
        return sensor
    if redis.sensor.load(get_sql(mac_address, sensor_id)):
        return get_redis(mac_address, sensor_id)
    return False

def fields(mac_address, sensor_id):
    data = []
    for name in redis.field.list(mac_address, sensor_id):
        data.append(redis.field.get(mac_address, sensor_id, name))
    return data

def update(mac_address, sensor_id, **kwargs):
    update_sql(mac_address, sensor_id, **kwargs)
    update_redis(mac_address, sensor_id, **kwargs)
    return True

def list(icpe):
    return SQL.session.query(SensorModel).join(SensorModel.icpe).\
            filter(iCPEModel.mac_address == icpe).all()

def load(*icpes):
    if not len(icpes):
        icpes = NodeDefender.db.icpe.list()
    
    for icpe in icpes:
        sensors = list(icpe.mac_address)
        for sensor in sensors:
            get(icpe.mac_address, sensor.sensor_id)
            if not sensor.product_name:
                NodeDefender.mqtt.command.sensor.\
                        sensor_info(icpe.mac_address, sensor.sensor_id)
    return True

def create(mac_address, sensor_id):
    if sensor_id == 'sys' or int(sensor_id) < 5:
        return False
    if not create_sql(mac_address, sensor_id):
        return False
    NodeDefender.mqtt.command.sensor.sensor_info(mac_address, sensor_id)
    NodeDefender.db.message.sensor_created(get_sql(mac_address, sensor_id))
    return get_redis(mac_address, sensor_id)

def delete(mac_address, sensor):
    delete_sql(mac_address, sensor)
    delete_redis(mac_address, sensor)
    return True
