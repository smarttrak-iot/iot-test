from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class DevModel(db.Model):
    
    devId = db.Column(db.String(20), primary_key=True)
    power = db.Column(db.Float(precision=2))
    voltage = db.Column(db.Float(precision=2))
    current = db.Column(db.Float(precision=2))
    def __init__(self, devId,power,voltage,current):
        self.devId = devId
        self.power = power
        self.voltage = voltage
        self.current = current

    def json(self):
        return {'devId': self.devId,'power': self.power,'voltage': self.voltage,'current': self.current}
