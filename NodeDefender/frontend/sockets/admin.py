from flask_socketio import emit, send
import NodeDefender

def load_sockets(socketio):
    socketio.on_event('general', general_info, namespace='/admin')
    socketio.on_event('logging', logging_info, namespace='/admin')
    socketio.on_event('database', database_info, namespace='/admin')
    socketio.on_event('celery', celery_info, namespace='/admin')
    socketio.on_event('mail', mail_info, namespace='/admin')
    socketio.on_event('mqttCreate', create_mqtt, namespace='/admin')
    socketio.on_event('mqttInfo', mqtt_info, namespace='/admin')
    socketio.on_event('mqttDeleteHost', delete_mqtt, namespace='/admin')
    socketio.on_event('mqttUpdateHost', update_mqtt, namespace='/admin')
    socketio.on_event('mqttList', list_mqtt, namespace='/admin')
    return True

def general_info():
    config = NodeDefender.config.general.config.copy()
    config['release'] = NodeDefender.release
    config['hostname'] = NodeDefender.hostname
    config['date_loaded'] = str(NodeDefender.date_loaded)
    config['uptime'] = NodeDefender.config.general.uptime()
    emit('general', config)
    return True

def logging_info():
    return emit('logging', NodeDefender.config.logging.config)

def database_info():
    return emit('database', NodeDefender.config.database.config)

def celery_info():
    return emit('celery', NodeDefender.config.celery.config)

def mail_info():
    return emit('mail', NodeDefender.config.mail.config)

def create_mqtt(host, port, group):
    try:
        NodeDefender.db.mqtt.create(host, port)
    except AttributeError as e:
        emit('error', e, namespace='/general')
    NodeDefender.db.group.add_mqtt(group, host, port)
    NodeDefender.mail.group.new_mqtt(group, host, port)
    NodeDefender.mqtt.connection.add(host, port)
    emit('reload', namespace='/general')
    return True

def list_mqtt(group):
    emit('list', NodeDefender.db.mqtt.list(group))
    return True

def mqtt_info(host, port):
    mqtt = NodeDefender.db.mqtt.get_redis(host, port)
    sql_mqtt = NodeDefender.db.mqtt.get_sql(host, port)
    mqtt['icpes'] = [icpe.mac_address for icpe in sql_mqtt.icpes]
    mqtt['groups'] = [group.name for group in sql_mqtt.groups]
    emit('mqttInfo', mqtt)
    return True

def update_mqtt(current_host, new_host):
    mqtt = NodeDefender.db.mqtt.get_sql(current_host['host'],
                                        current_host['port'])
    mqtt.host = new_host['host']
    mqtt.port = new_host['port']
    NodeDefender.db.mqtt.save_sql(mqtt)
    emit('reload', namespace='/general')
    return True

def delete_mqtt(host, port):
    NodeDefender.db.mqtt.delete(host, port)
    emit('reload', namespace='/general')
    return True
