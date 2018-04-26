from NodeDefender.db.sql import SQL
from datetime import datetime
from NodeDefender.db.sql.node import LocationModel
import NodeDefender
from flask import url_for

class MessageModel(SQL.Model):
    '''
    Representing one group containing iCPEs and Users
    '''
    __tablename__ = 'message'
    id = SQL.Column(SQL.Integer, primary_key=True)
    date = SQL.Column(SQL.DateTime)
    subject = SQL.Column(SQL.String(50))
    body = SQL.Column(SQL.String(180))
    
    group_id = SQL.Column(SQL.Integer, SQL.ForeignKey('group.id'))
    user_id = SQL.Column(SQL.Integer, SQL.ForeignKey('user.id'))
    node_id = SQL.Column(SQL.Integer, SQL.ForeignKey('node.id'))
    icpe_id = SQL.Column(SQL.Integer, SQL.ForeignKey('icpe.id'))
    sensor_id = SQL.Column(SQL.Integer, SQL.ForeignKey('sensor.id'))


    def __init__(self, subject, body):
        self.subject = subject
        self.body = body
        self.date = datetime.now()

    def to_json(self):
        if self.group:
            group = self.group.name
            url = url_for('admin_view.admin_group', name =
                          NodeDefender.serializer.dumps(group))
            icon = 'fa fa-users fa-3x'
        else:
            group = False
        
        if self.user:
            user = self.user.email
            url = url_for('admin_view.admin_user', email =
                          NodeDefender.serializer.dumps(user))
            icon = 'fa fa-user fa-3x'
        else:
            user = False

        if self.node:
            node = self.node.name
            url = url_for('node_view.nodes_node', name =
                          NodeDefender.serializer.dumps(node))
            icon = 'fa fa-map-marker fa-3x'
        else:
            node = False

        if self.icpe:
            icpe = self.icpe.name
            url = "#"
            icon = 'fa fa-bug fa-3x'
        else:
            icpe = False

        if self.sensor:
            sensor = self.sensor.name
            url = "#"
            icon = 'fa fa-bug fa-3x'
        else:
            sensor = False

        return {'group' : group, 'user' : user,\
                'node' : node, 'icpe' : icpe, 'sensor' : sensor,\
                'subject' : self.subject,
                'body' : self.body,
                'date' : str(self.date),
                'icon' : icon, 'url' : url}
