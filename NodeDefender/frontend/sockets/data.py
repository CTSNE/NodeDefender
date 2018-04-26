from flask_socketio import emit, send, disconnect, join_room, leave_room, \
        close_room, rooms
from flask_login import current_user
import NodeDefender

def load_sockets(socketio):
    socketio.on_event('messages', messages, namespace='/data')
    socketio.on_event('groupMessages', group_messages, namespace='/data')
    socketio.on_event('nodeMessages', node_messages, namespace='/data')
    socketio.on_event('userMessages', user_messages, namespace='/data')
    socketio.on_event('groupEventsAverage', group_event_average, namespace='/data')
    socketio.on_event('groupEventsList', group_event_list, namespace='/data')
    socketio.on_event('nodeEvents', node_events, namespace='/data')
    socketio.on_event('sensorEvents', sensor_events, namespace='/data')
    socketio.on_event('groupPowerAverage', group_power_average, namespace='/data')
    socketio.on_event('nodePowerAverage', node_power_average, namespace='/data')
    socketio.on_event('nodePowerCurrent', node_power_current, namespace='/data')
    socketio.on_event('sensorPowerAverage', sensor_power_average, namespace='/data')
    socketio.on_event('groupHeatAverage', group_heat_average, namespace='/data')
    socketio.on_event('nodeHeatAverage', node_heat_average, namespace='/data')
    socketio.on_event('nodeHeatCurrent', node_heat_current, namespace='/data')
    socketio.on_event('sensorHeatAverage', sensor_heat_average, namespace='/data')
    return True

# Messages
def messages():
    messages = NodeDefender.db.message.messages(current_user)
    return emit('messages', ([message.to_json() for message in messages]))

def group_messages(group):
    messages = NodeDefender.db.message.group_messages(group)
    return emit('messages', ([message.to_json() for message in messages]))

def node_messages(node):
    messages = NodeDefender.db.message.node_messages(node)
    return emit('messages', ([message.to_json() for message in messages]))

def user_messages(user):
    return emit('messages', NodeDefender.db.message.messages(user))

# Events
def group_event_average(group, length = None):
    events = NodeDefender.db.data.group.event.average(group)
    emit('groupEventsAverage', events)
    return True

def group_event_list(groups, length):
    events = NodeDefender.db.data.group.event.list(groups, length)
    if events:
        events = [event.to_json() for event in events]
        emit('groupEventsList', events)
    return True

def node_events(msg):
    events = NodeDefender.db.data.node.event.get(msg['node'], msg['length'])
    if events:
        emit('nodeEvents', ([event.to_json() for event in events]))
    return True

def sensor_events(msg):
    events = NodeDefender.db.data.sensor.event.get(msg['icpe'], msg['sensor'])
    if events:
        emit('sensorEvents', ([event.to_json() for event in events]))
    return True

# Power
def group_power_average(group):
    data = NodeDefender.db.data.group.power.average(group)
    emit('groupPowerAverage', (data))
    return True

def node_power_average(node):
    data = NodeDefender.db.data.node.power.average(node)
    emit('nodePowerAverage', data)
    return True

def node_power_current(node):
    data = NodeDefender.db.data.node.power.current(node)
    emit('nodePowerCurrent', data)
    return True

def sensor_power_average(msg):
    data = NodeDefender.db.data.sensor.power.average(msg['icpe'], msg['sensor'])
    emit('sensorPowerAverage', (data))
    return True


# Heat
def group_heat_average(group):
    data = NodeDefender.db.data.group.heat.average(group)
    emit('groupHeatAverage', (data))
    return True

def node_heat_average(node):
    data = NodeDefender.db.data.node.heat.average(node)
    emit('nodeHeatAverage', (data))
    return True

def node_heat_current(node):
    data = NodeDefender.db.data.node.heat.current(node)
    emit('nodeHeatCurrent', data)
    return True

def sensor_heat_average(msg):
    data = NodeDefender.db.data.sensor.heat.average(msg['icpe'], msg['sensor'])
    emit('sensorHeatAverage', (data))
    return True
