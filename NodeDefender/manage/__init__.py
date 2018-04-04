from flask_script import Manager, Command
from flask_migrate import Migrate, MigrateCommand
import NodeDefender
from NodeDefender.manage.user import manager as UserManager
from NodeDefender.manage.role import manager as RoleManager
from NodeDefender.manage.group import manager as GroupManager
from NodeDefender.manage.node import manager as NodeManager
from NodeDefender.manage.icpe import manager as iCPEManager
from NodeDefender.manage.sensor import manager as SensorManager
from NodeDefender.manage.mqtt import manager as MQTTManager
from NodeDefender.manage.setup import manager as SetupManager

app = NodeDefender.create_console_app()

manager = Manager(app)

@manager.command
def run():
    app = NodeDefender.create_app()
    try:
        port = int(NodeDefender.app.config['SERVER_PORT'])
    except KeyError:
        port = 5000
    NodeDefender.socketio.run(app, host="0.0.0.0", port=port)

manager.add_command('user', UserManager)
manager.add_command('role', RoleManager)
manager.add_command('group', GroupManager)
manager.add_command('node', NodeManager)
manager.add_command('iCPE', iCPEManager)
manager.add_command('sensor', SensorManager)
manager.add_command('mqtt', MQTTManager)
manager.add_command('setup', SetupManager)

migrate = Migrate(app, NodeDefender.db.sql.SQL)
manager.add_command('db', MigrateCommand)

def console():
    manager.run()
