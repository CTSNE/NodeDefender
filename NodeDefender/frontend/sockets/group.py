from flask_socketio import emit, send, disconnect, join_room, leave_room, \
        close_room, rooms
import NodeDefender
from flask_login import current_user
from flask import url_for
from geopy.geocoders import Nominatim

def load_sockets(socketio):
    socketio.on_event('create', create, namespace='/group')
    socketio.on_event('list', list_groups, namespace='/group')
    socketio.on_event('delete', delete, namespace='/group')
    socketio.on_event('coordinates', coordinates, namespace='/group')
    socketio.on_event('info', info, namespace='/group')
    socketio.on_event('update', update, namespace='/group')
    socketio.on_event('updateLocation', update_location, namespace='/group')
    socketio.on_event('addUser', add_user, namespace='/group')
    socketio.on_event('removeUser', remove_user, namespace='/group')


def create(name, email, location):
    if NodeDefender.db.group.get(name):
        emit('error', ('Group exsists'), namespace='/general')
        return False
    group = NodeDefender.db.group.create(name, email)
    NodeDefender.db.group.location(name, **location)
    NodeDefender.mail.group.new_group(name)
    url = url_for('admin_view.admin_group', name = NodeDefender.serializer.dumps(name))
    return emit('redirect', (url), namespace='/general')

def list_groups(user = None):
    if user is None:
        user = current_user.email
    return emit('list',  [group.name for group in
                      NodeDefender.db.group.list(user_mail = user)])

def delete(name):
    NodeDefender.db.group.delete(name)
    url = url_for('admin_view.admin_groups')
    return emit('redirect', (url), namespace='/general')

def coordinates(street, city):
    geo = Nominatim()
    coords = geo.geocode(street + ' ' + city)
    if coords:
        emit('coordinates', (coords.latitude, coords.longitude))
    else:
        emit('error', "Coordinates not found", namespace='/general')

def info(name):
    group = NodeDefender.db.group.get(name)
    if group:
        group = group.to_json()
        return emit('info', group)
    else:
        return emit('error', 'Group {} not found'.format(name), namespace='/general')

def update(name, kwargs):
    group = NodeDefender.db.group.update(name, **kwargs)
    url = url_for('admin_view.admin_group', name =
                  NodeDefender.serializer.dumps(group.name))
    return emit('redirect', (url), namespace='/general')

def update_location(name, address):
    NodeDefender.db.group.location(name, **address)
    return emit('reload', namespace='/general')

def add_user(group_name, user_mail):
    NodeDefender.db.group.add_user(group_name, user_mail)
    return emit('reload', namespace='/general')

def remove_user(group_name, user_mail):
    NodeDefender.db.group.remove_user(group_name, user_mail)
    return emit('reload', namespace='/general')
