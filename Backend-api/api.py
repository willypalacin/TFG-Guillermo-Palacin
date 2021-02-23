from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort
from IOSRouter import IOSRouter
from AristaSwitch import AristaSwitch
from JunosOSRouter import JunosOSRouter
import json

app = Flask(__name__)
api = Api(app)

devices = []

device_post = reqparse.RequestParser()
device_post.add_argument("name", type=str, help="Name of the device", required=True)
device_post.add_argument("ip", type=str, help="ip/mask is required to make the put request", required=True)
device_post.add_argument("type", type=str, help="type of device ej: cisco-ios", required=True)
device_post.add_argument("usnm", type=str, help="username", required=True)
device_post.add_argument("pass", type=str, help="type of device ej: cisco-ios", required=True)
device_post.add_argument("port", type=str, help="type of device ej: cisco-ios", required=True)

#device_put = reqparse.RequestParser()
#args = device_put.parse_args()
#device_put.add_argument("property", type=str, help="type of device ej: cisco-ios", required=True)
#device_put.add_argument("ip", type=str, help="username", required=True)
#device_put.add_argument("mask", type=str, help="type of device ej: cisco-ios", required=True)
#device_put.add_argument("description", type=str, help="type of device ej: cisco-ios", required=True)


def errorHandler(video_id):
    if video_id not in videos:
        #Automaticamente devuelve la respuesta
        abort(404,message="Video no es valido")

def getDeviceByName(name):
    for device in devices:
        if device.getName() == name:
            return device


class DeviceAddHandler(Resource):
    def addDeviceByType(self, args):
        if args["type"] == 'cisco_ios':
            device = IOSRouter(args["name"], args["ip"], args["type"], args["usnm"], args["pass"], args["port"])
            return device
        if args["type"] == 'arista_eos':
            device = AristaSwitch(args["name"], args["ip"], args["type"], args["usnm"], args["pass"], args["port"])
            return device
        if args["type"] == 'junos_os':
            device = JunosOSRouter(args["name"], args["ip"], args["type"], args["usnm"], args["pass"], args["port"])

            return device
        return 0

    def get(self, device_name):
        errorHandler(device_name)
        return devices[device_name]

    def post(self, device_name):

        args = device_post.parse_args()

        device = self.addDeviceByType(args)
        print("DEICE NAME: " + device.getType())

        status_code = device.checkConnectivity()
        devices.append(device) #Solo en caso de que el status code sea satisfactorio
        #device.createLoopbackTesting("1.2.3.4", "255.255.255.255", , "Loopback 1242")
        return "hola", status_code
        #devices[device_name] = args
        #return  devices[device_name], 201
    def delete(self, device_name):
        errorHandler( device_name)
        devices.pop(device_name)
        return 'Dispositivo eliminado',204



class DeviceAddPropertyHandler(Resource):
    def put(self, device_name, property):
        #args = device_put.parse_args()
        device = getDeviceByName(device_name)
        print (request.is_json)
        args = json.loads(request.data)
        #device.createLoopbackTesting("Loopback123", device_name, '1.2.2.1', '255.255.255.0')

        device.editInterface(args["int_name"], args["description"], args["ip"], args["mask"])
        return "Correcto", 200



    #def post(self):
    #    return {"data": "Hello World_Post"}



if __name__ == '__main__':
    api.add_resource(DeviceAddHandler, "/device/<string:device_name>")
    api.add_resource(DeviceAddPropertyHandler, "/device/<string:device_name>/<string:property>")
    app.run(debug=True)
