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
device_post.add_argument("name", type=str, help="Nombre del dispositivo", required=True)
device_post.add_argument("ip", type=str, help="ip/mask se necesita para hacer la peticion", required=True)
device_post.add_argument("type", type=str, help="tipo dispositivo cisco-ios", required=True)
device_post.add_argument("usnm", type=str, help="username", required=True)
device_post.add_argument("pass", type=str, help="password", required=True)
device_post.add_argument("port", type=str, help="puerto ", required=True)



def errorHandler(video_id):
    if video_id not in videos:
        #Automaticamente devuelve la respuesta
        abort(404,message="Video no es valido")

def getDeviceByName(name):
    for device in devices:
        if device.getName() == name:
            return device

@app.route('/device/<string:device_name>/interfaces/list',methods = ['GET'])
def getInterfacesList(device_name):
    device = getDeviceByName(device_name)
    interfaces, status_code = device.getInterfacesList()
    return interfaces, status_code

@app.route('/devices/show/interfaces/all',methods = ['GET'])
def getShowInterfaces():
    data = {}
    for device in devices:
        data[device.getName()] = device.showInterfaces()
    return data, 201

@app.route('/devices/show/ip/route',methods = ['GET'])
def getShowIpRoute():
    data = {}
    for device in devices:
        data[device.getName()] = device.showIpRoute()
    return data, 201

@app.route('/devices/show/vlan',methods = ['GET'])
def getShowVlan():
    data = {}
    for device in devices:
        data[device.getName()] = device.showVlan()
    return data, 201

@app.route('/devices/show/ospf/neighbors',methods = ['GET'])
def getShowOspfNeigh():
    data = {}
    for device in devices:
        data[device.getName()] = device.showOspfNeigh()
        print(device.showOspfNeigh)
        print (data)
    return data, 201

@app.route('/device/<string:device_name>/protocols/ospf',methods = ['GET'])
def getOspfData(device_name):
    device = getDeviceByName(device_name)
    data, code = device.getOspfData()
    return data, code

@app.route('/device/<string:device_name>/protocols/ospf',methods = ['PUT'])
def addOspf(device_name):
    args = json.loads(request.data)
    device = getDeviceByName(device_name)
    msg, code = device.createOspf(args)
    return msg, code

@app.route('/device/<string:device_name>/n2/vlans',methods = ['PUT'])
def addVlans(device_name):
    args = json.loads(request.data)
    device = getDeviceByName(device_name)
    msg, code = device.createVlans(args)
    print(args)
    return msg, code

@app.route('/device/<string:device_name>/ha/vrrp',methods = ['PUT'])
def addVrrp(device_name):
    args = json.loads(request.data)
    device = getDeviceByName(device_name)
    msg, code = device.createVrrp(args)
    return msg, code

@app.route('/device/<string:device_name>/n2/lacp',methods = ['PUT'])
def addPortChannel(device_name):
    args = json.loads(request.data)
    device = getDeviceByName(device_name)
    msg, code = device.createPortChannel(args)
    return msg, code

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
            print (args['type'])
            return device
        return 0

    def get(self, device_name):
        errorHandler(device_name)
        return devices[device_name]

    def post(self, device_name):

        args = device_post.parse_args()

        device = self.addDeviceByType(args)

        status_code, msg = device.checkConnectivity()
        if status_code == 201:
            devices.append(device) #Solo en caso de que el status code sea satisfactorio
        #device.createLoopbackTesting("1.2.3.4", "255.255.255.255", , "Loopback 1242")
        return msg, status_code
        #devices[device_name] = args
        #return  devices[device_na åme], 201
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
    api.add_resource(DeviceAddPropertyHandler, "/device/<string:device_name>/interfaces/<string:property>")
    app.run(debug=True)
