from jnpr.junos import Device
from jnpr.junos import Device
from lxml import etree
import json
import jxmlease
import pprint
from ncclient import manager, xml_

showVrrp = []

try:
    dev = Device(host='66.129.235.12', user='jcluser', passwd='Juniper!1', port=32003)
    dev.open()
    showOspfInt = []
    rpc = dev.rpc.get_vrrp_information({'format':'json'}, extensive=True)
    for intf in rpc['vrrp-information'][0]['vrrp-interface']:
        data = {
            'interface': intf['interface'][0]['data'],
            'group': intf['group'][0]['data'],
            'state': intf['vrrp-state'][0]['data'],
            'time': intf['advertisement-timer'][0]['data'],
            'master_ip': intf['master-router'][0]['data'],
            'group_ip': intf['preempt-hold'][0]['vip'][0]['data']
        }
        showVrrp.append(data)
except Exception as e:
    print(e)
