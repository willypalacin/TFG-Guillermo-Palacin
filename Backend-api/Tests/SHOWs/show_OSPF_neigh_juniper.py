
from jnpr.junos import Device
from jnpr.junos import Device
from lxml import etree
import json
import jxmlease
import pprint

dev = Device(host='66.129.235.12', user='jcluser', passwd='Juniper!1', port=30003)
dev.open()

rpc = dev.rpc.get_ospf_neighbor_information({'format':'json'}, extensive=True)

showOspfNeigh = []

for neigh in rpc['ospf-neighbor-information'][0]['ospf-neighbor']:
    data = {
        'neighbor_id': neigh['neighbor-id'][0]['data'],
        'priority': neigh['neighbor-priority'][0]['data'],
        'state':  neigh['ospf-neighbor-state'][0]['data'],
        'dead_time': neigh['activity-timer'][0]['data'],
        'address': neigh['neighbor-address'][0]['data'],
        'interface': neigh['interface-name'][0]['data'] }
    showOspfNeigh.append(data)

print(showOspfNeigh)
