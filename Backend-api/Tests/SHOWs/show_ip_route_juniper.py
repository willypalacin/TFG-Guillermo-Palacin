from jnpr.junos import Device
from jnpr.junos import Device
from lxml import etree
import json
import jxmlease
import pprint
from jnpr.junos.op.routes import RouteTable

dev = Device(host='192.168.1.222', user='root', passwd='tfgtfg1', port=830)
dev.open()

showIpRoute = []

#showIpRoute.append(data)
rpc = dev.rpc.get_route_information({'format':'json'})
#rpc_xml = etree.tostring(rpc, pretty_print=True, encoding='unicode')
for route in rpc['route-information'][0]['route-table']:
    for rt in route['rt']:
        data = {
                'protocolo' : '',
                'red' : '',
                'distancia': '',
                'metrica': '',
                'gateway': '',
                'gateway_if': ''
        }
        data['red'] = rt['rt-destination'][0]['data'] #red
        data['protocolo'] = rt['rt-entry'][0]['protocol-name'][0]['data'] #protocolo
        if "metric" in rt['rt-entry'][0].keys():
            data['metrica'] = rt['rt-entry'][0]['metric'][0]['data']
        else:
            print('')
        if "preference" in rt['rt-entry'][0].keys():
            data['distancia'] = rt['rt-entry'][0]['preference'][0]['data']
        if "nh" in rt['rt-entry'][0].keys():
            if "to" in rt['rt-entry'][0]['nh'][0].keys():
                data['gateway'] = rt['rt-entry'][0]['nh'][0]['to'][0]['data']
            if "via" in rt['rt-entry'][0]['nh'][0].keys():
                data['gateway_if'] = rt['rt-entry'][0]['nh'][0]['via'][0]['data']
        showIpRoute.append(data)
print(showIpRoute)
