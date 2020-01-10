from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

from models.testmodel import db,DevModel



#devices = []

class Dev(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('power',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('voltage',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('current',
        type=float,
        required=True,
        help="This field cannot be left blank!"
        )


    def get(self,devId):
        device =  DevModel.query.filter_by(devId=devId).first()
        if device:
            return device.json()
        return {'message': 'device not found'}, 404


    def post(self,devId):
        if DevModel.query.filter_by(devId=devId).first():
            return {'message': "A device with id '{}' already exists.".format(devId)}
        data = Dev.parser.parse_args()
        #device = {'devId':devId,'power':data['power'],'voltage':data['voltage'],'current':data['current']}
        device = DevModel(devId,data['power'],data['voltage'],data['current'])

        #devices.append(device)
        #return device
        try:
            db.session.add(device)
            db.session.commit()
        except:
            return {"message": "An error occurred inserting the device."}, 500

        return device.json(), 201

    def put(self,devId):
        data = Dev.parser.parse_args()

        #device = next(filter(lambda x: x['devId'] == devId,devices), None)
        device = DevModel.query.filter_by(devId=devId).first()

        if device is None:
            device = DevModel(devId,data['power'],data['voltage'],data['current'])
        else:
            device.power = data['power']
            device.voltage = data['voltage']
            device.current = data['current']

            db.session.add(device)
            db.session.commit()

        return device.json()


class DeviceList(Resource):
    def get(self):
        return {'devices': list(map(lambda x: x.json(), DevModel.query.all()))}
        #return{'devices':devices}

api.add_resource(Dev,'/device/<string:devId>')
api.add_resource(DeviceList,'/devices')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
