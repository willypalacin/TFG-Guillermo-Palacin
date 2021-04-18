from jnpr.junos import Device
from jnpr.junos import Device
from lxml import etree
import json
import jxmlease
import pprint
from jnpr.junos.op.routes import RouteTable

dev = Device(host='192.168.1.233', user='root', passwd='tfgtfg1', port=830)
dev.open()



#showIpRoute.append(data)
#rpc = dev.rpc.get_route_information({'format':'json'})
interfaces=[]

data = dev.rpc.get_config(options={'format':'json'})
for intf in data['configuration']['interfaces']['interface']:
    print(intf)
    if ":" not in intf['name'] and int['name'] not in :
        interface ='{}'.format(intf['name'])
        interfaces.append(interface)
    #print(data['configuration']['interfaces'][intf])
print(interfaces)
