from ... import db


class StatisticsModel(db.Model):
    __tablename__ = 'statistics'
    id = db.Column(db.Integer, primary_key=True)
    
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    node_id = db.Column(db.Integer, db.ForeignKey('node.id'))
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))

    hourly = db.relationship('HourlyStatisticsModel', backref='statisticshourly')
    daily = db.relationship('DailyStatisticsModel', backref='statisticsdaily')
    weekly = db.relationship('WeeklyStatisticsModel', backref='statisticsweekly')
    
    def __init__(self):
        pass



class HourlyStatisticsModel(db.Model):
    __tablename__ = 'hourlystatistics'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('statistics.id'))

    heat = db.relationship('HeatStatModel', backref='hourlystatisticsheat')
    power = db.relationship('PowerStatModel', backref='hourlystatisticspower')
    events = db.relationship('EventStatModel', backref='hourlystatisticsevents')
    
    last_updated = db.Column(db.DateTime)

    def __init__(self):
        last_updated = datetime.now()

class DailyStatisticsModel(db.Model):
    __tablename__ = 'dailystatistics'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('statistics.id'))

    heat = db.relationship('HeatStatModel', backref='dailystatisticsheat')
    power = db.relationship('PowerStatModel', backref='dailystatisticspower')
    events = db.relationship('EventStatModel', backref='dailystatisticsevents')
 
    last_updated = db.Column(db.DateTime)

    def __init__(self):
        last_updated = datetime.now()

class WeeklyStatisticsModel(db.Model):
    __tablename__ = 'weeklystatistics'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('statistics.id'))
    
    heat = db.relationship('HeatStatModel', backref='weeklystatisticsheat')
    power = db.relationship('PowerStatModel', backref='weeklystatisticspower')
    events = db.relationship('EventStatModel', backref='weeklystatisticsevents')
    
    last_updated = db.Column(db.DateTime)

    def __init__(self):
        self.last_updated = datetime.now()

'''
Statistics Model
'''

class HeatStatModel(db.Model):
    __tablename__ = 'heatstat'
    id = db.Column(db.Integer, primary_key=True)
    hourly_id = db.Column(db.Integer, db.ForeignKey('hourlystatistics.id'))
    daily_id = db.Column(db.Integer, db.ForeignKey('dailystatistics.id'))
    weekly_id = db.Column(db.Integer, db.ForeignKey('weeklystatistics.id'))

    high = db.Column(db.Float)
    low = db.Column(db.Float)
    average = db.Column(db.Float)

    def __init__(self):
        pass

class PowerStatModel(db.Model):
    __tablename__ = 'powerstat'
    id = db.Column(db.Integer, primary_key=True)
    hourly_id = db.Column(db.Integer, db.ForeignKey('hourlystatistics.id'))
    daily_id = db.Column(db.Integer, db.ForeignKey('dailystatistics.id'))
    weekly_id = db.Column(db.Integer, db.ForeignKey('weeklystatistics.id'))

    high = db.Column(db.Float)
    low = db.Column(db.Float)
    average = db.Column(db.Float)

    def __init__(self):
        pass

class EventStatModel(db.Model):
    __tablename__ = 'eventstat'
    id = db.Column(db.Integer, primary_key=True)
    hourly_id = db.Column(db.Integer, db.ForeignKey('hourlystatistics.id'))
    daily_id = db.Column(db.Integer, db.ForeignKey('dailystatistics.id'))
    weekly_id = db.Column(db.Integer, db.ForeignKey('weeklystatistics.id'))
  
    respond = db.Column(db.Integer)
    report = db.Column(db.Integer)
    command = db.Column(db.Integer)

    critcial = db.Column(db.Integer)
    normal = db.Column(db.Integer)

    def __init__(self):
        pass