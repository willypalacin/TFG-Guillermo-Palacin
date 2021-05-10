from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort
from IOSRouter import IOSRouter
from AristaSwitch import AristaSwitch
from JunosOSRouter import JunosOSRouter
import json
import yaml

app = Flask(__name__)
api = Api(app)

devices = []






def getDeviceByName(name):
    for device in devices:
        if device.getName() == name:
            return device

def addDeviceByType(args):
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

@app.route('/devices/names',methods = ['GET'])
def getDevices():
    devs = {}
    for device in devices:
        devs[device.getName()] = "up"
    return devs, 201

@app.route('/device/<string:device_name>/ospf',methods = ['GET'])
def getOspfData(device_name):
    device = getDeviceByName(device_name)
    data, code = device.getOspfData()
    return data, code

@app.route('/device/<string:device_name>/ospf/neighbors',methods = ['GET'])
def getShowOspfNeigh(device_name):
    data = {}
    device = getDeviceByName(device_name)
    data[device.getName()] = device.showOspfNeigh()
    return data, 201

@app.route('/device/<string:device_name>/ospf/interfaces',methods = ['GET'])
def getShowOspfIntf(device_name):
    data = {}
    device = getDeviceByName(device_name)
    data[device.getName()] = device.showOspfIntf()
    return data, 201

@app.route('/device/<string:device_name>/switchport',methods = ['PUT'])
def addSwitchPort(device_name):
    device = getDeviceByName(device_name)
    data, code = device.createSwitchPort(json.loads(request.data))
    return data, code

@app.route('/device/<string:device_name>/vrrp',methods = ['GET'])
def getVrrpData(device_name):
    device = getDeviceByName(device_name)
    data = {}
    data[device.getName()] = device.showVrrp()
    return data, 201

@app.route('/device/<string:device_name>/ospf',methods = ['PUT'])
def addOspf(device_name):
    args = json.loads(request.data)
    device = getDeviceByName(device_name)
    msg, code = device.createOspf(args)
    return msg, code

@app.route('/device/<string:device_name>/interfaces',methods = ['PUT'])
def addInterface(device_name):
    args = json.loads(request.data)
    device = getDeviceByName(device_name)
    msg, code = device.editInterface(args["int_name"], args["description"], args["ip"], args["mask"])
    return msg, code

@app.route('/device/<string:device_name>/interfaces',methods = ['GET'])
def getShowInterfaces(device_name):
    data = {}
    device = getDeviceByName(device_name)
    data[device.getName()] = device.showInterfaces()
    return data, 201


@app.route('/device/<string:device_name>/acl',methods = ['PUT'])
def addAcl(device_name):
    args = json.loads(request.data)
    device = getDeviceByName(device_name)
    msg, code = device.createAcl(args)
    return msg, code

@app.route('/device/<string:device_name>/vlans',methods = ['GET'])
def getShowVlan(device_name):
    data = {}
    device = getDeviceByName(device_name)
    data[device.getName()] = device.showVlan()
    return data, 201

@app.route('/device/<string:device_name>/vlans',methods = ['PUT'])
def addVlans(device_name):
    args = json.loads(request.data)
    device = getDeviceByName(device_name)
    msg, code = device.createVlans(args)
    print(args)
    return msg, code

@app.route('/device/<string:device_name>/vrrp',methods = ['PUT'])
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

@app.route('/device/<string:device_name>/route',methods = ['GET'])
def getShowIpRoute(device_name):
    device = getDeviceByName(device_name)
    data = {}
    data[device.getName()] = device.showIpRoute()
    return data, 201

@app.route('/device/<string:device_name>/static',methods = ['PUT'])
def addStaticRouting(device_name):
    args = json.loads(request.data)
    device = getDeviceByName(device_name)
    msg, code = device.createStaticRouting(args)
    return msg, code

@app.route('/device/<string:device_name>',methods = ['POST'])
def addDevice(device_name):
    device_post = reqparse.RequestParser()
    device_post.add_argument("name", type=str, help="Nombre del dispositivo", required=True)
    device_post.add_argument("ip", type=str, help="ip/mask se necesita para hacer la peticion", required=True)
    device_post.add_argument("type", type=str, help="tipo dispositivo cisco-ios", required=True)
    device_post.add_argument("usnm", type=str, help="username", required=True)
    device_post.add_argument("pass", type=str, help="password", required=True)
    device_post.add_argument("port", type=str, help="puerto ", required=True)
    args = device_post.parse_args()
    device = addDeviceByType(args)
    status_code, msg = device.checkConnectivity()
    if status_code == 201:
            devices.append(device) #Solo en caso de que el status code sea satisfactorio
    return msg, status_code


if __name__ == '__main__':
    #api.add_resource(DeviceAddPropertyHandler, "/device/<string:device_name>/interfaces/<string:property>")
    app.run(debug=True)
