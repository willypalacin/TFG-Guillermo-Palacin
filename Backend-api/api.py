from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from Device import Device

app = Flask(__name__)
api = Api(app)

devices = {}

device_put = reqparse.RequestParser()
#device_put.add_argument("name", type=str, help="Name of the device", required=True)
device_put.add_argument("ip", type=str, help="ip/mask is required to make the put request", required=True)
device_put.add_argument("type", type=str, help="type of device ej: cisco-ios", required=True)
device_put.add_argument("usnm", type=str, help="username", required=True)
device_put.add_argument("pass", type=str, help="type of device ej: cisco-ios", required=True)
device_put.add_argument("port", type=str, help="type of device ej: cisco-ios", required=True)


def errorHandler(video_id):
    if video_id not in videos:
        #Automaticamente devuelve la respuesta
        abort(404,message="Video no es valido")



class DeviceRequestHandler(Resource):
    def get(self, device_name):
        errorHandler(device_name)
        return devices[device_name]

    def put(self, device_name):
        args = device_put.parse_args()
        device = Device(device_name, args["ip"], args["type"], args["usnm"], args["pass"], args["port"])
        status_code = device.checkConnectivity()
        #device.createLoopbackTesting("1.2.3.4", "255.255.255.255", , "Loopback 1242")
        return "hola", status_code
        #devices[device_name] = args
        #return  devices[device_name], 201
    def delete(self, device_name):
        errorHandler( device_name)
        devices.pop(device_name)
        return 'Dispositivo eliminado',204



    #def post(self):
    #    return {"data": "Hello World_Post"}



if __name__ == '__main__':
    api.add_resource(DeviceRequestHandler, "/device/<string:device_name>")
    app.run(debug=True)
