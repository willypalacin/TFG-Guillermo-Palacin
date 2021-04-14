
from jnpr.junos import Device
from jnpr.junos import Device
from lxml import etree
import json
import jxmlease
import pprint

dev = Device(host='192.168.1.233', user='root', passwd='tfgtfg1', port=830)
dev.open()
#rsp = dev.rpc.get_interface_information(terse=True, normalize=True)
#rpc_xml = etree.tostring(rsp, pretty_print=True, encoding='unicode')
#xmlparser = jxmlease.Parser()
#result = jxmlease.parse(rpc_xml)

rpc = dev.rpc.get_interface_information(terse=True, normalize=True)
rpc_xml = etree.tostring(rpc, pretty_print=True, encoding='unicode')

interfaces = rpc.findall('.//physical-interface')
showInterfaces = {}

for intf in interfaces:
    try:
        nom = intf.find('./name').text
        adminStatus = intf.find('./logical-interface/admin-status').text
        proStatus = intf.find('./logical-interface/oper-status').text
        ip = "-"
        try:
            ip = intf.find('./logical-interface/address-family/interface-address/ifa-local').text
        except:
            pass
        showInterfaces[nom] = {
                'adminStatus' : adminStatus,
                'proStatus' : proStatus,
                'ip' : ip,
            }
    except:
        pass
print (showInterfaces)
