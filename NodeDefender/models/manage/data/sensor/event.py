from datetime import datetime, timedelta
from ....SQL import EventModel, iCPEModel, SensorModel
from ... import icpe as iCPESQL
from ... import sensor as SensorSQL
from ... import cmdclass as CmdclassSQL
from ..... import db
from ....redis import field as FieldRedis

def Latest(icpe, sensor):
    return EventModel.query.join(iCPEModel).join(SensorModel).\
            filter(iCPEModel.macaddr == icpe).\
            filter(SensorModel.macaddr == sensor).first()

def Get(icpe, sensor, limit = None):
    if limit is None:
        limit = 10
    return db.session.query(EventModel).\
            join(EventModel.sensor).\
            join(EventModel.icpe).\
            filter(iCPEModel.macaddr == icpe).\
            filter(SensorModel.sensorid == sensor).\
            order_by(EventModel.date.desc()).limit(int(limit)).all()

def Put(icpe, sensor, cmdclass, classtype, classevent, value):
    icpe = iCPESQL.Get(icpe)
    sensor = SensorSQL.Get(icpe.macaddr, sensor)
    cmdclass = CmdclassSQL.Get(icpe.macaddr, sensor.sensorid, cmdclass)
    event = EventModel(classtype, classevent, value)
    event.node = icpe.node
    event.icpe = icpe
    event.sensor = sensor
    event.sensorclass = cmdclass
    db.session.add(event)
    db.session.commit()
    FieldEvent(event)
    FieldRedis.Update(event)
