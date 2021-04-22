from jnpr.junos import Device
from jnpr.junos import Device
from lxml import etree
import json
import jxmlease
import pprint



dev = Device(host='66.129.235.11', user='jcluser', passwd='Juniper!1', port=41003)
dev.open()
showOspfInt = []
rpc = dev.rpc.get_ospf_interface_information({'format':'json'}, extensive=True)
for intf in rpc['ospf-interface-information'][0]['ospf-interface']:
    data = {'interface': '',
            'area': '',
            'ip_address_mask': '',
            'cost': '',
            'state': '',
            'neighbors_fc': '0/0'}
    data['interface'] = intf['interface-name'][0]['data']
    data['area'] = intf['ospf-area'][0]['data']
    data['state'] = intf['ospf-interface-state'][0]['data']
    data['cost'] = intf['interface-cost'][0]['data']
    data['ip_address_mask'] = intf['interface-address'][0]['data']
    showOspfInt.append(data)
print(showOspfInt)
