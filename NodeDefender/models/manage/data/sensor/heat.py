from datetime import datetime, timedelta
from ....SQL import HeatModel
from .. import icpe as iCPEData

def Latest(icpe, sensor):
    return HeatModel.query.filter_by(node = None, icpe = icpe, sensor = sensor).first()

def Get(icpe, sensor, from_date = (datetime.now() - timedelta(days=7)), to_date =
        datetime.now()):
    return session.query(HeatModel).filter(node == None, icpe == icpe,\
                                           sensor == sensor, date > from_date,\
                                           date < to_date)

def Put(icpe, sensor, heat, date = datetime.now()):
    date = date.replace(minute=0, second=0, microsecond=0)
    data = PowerModel.query.join(iCPEModel).join(SensorModel).\
            filter(PowerModel.date == date).\
            filter(iCPEModel.macaddr == icpe).\
            filter(SensorModel.sensorid == sensor).first()

    if data:
        data.heat = (data.heat / 2)
        data.precision += 1
    else:
        data = PowerModel(icpe = icpe, sensor = sensor, heat = heat, date = date)
    db.session.add(data)
    db.session.commit()
    iCPEData.heat.Put(icpe, heat, date)
