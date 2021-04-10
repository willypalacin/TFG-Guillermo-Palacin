
from jnpr.junos import Device
from lxml import etree
import json
import jxmlease

dev = Device(host='66.129.235.13', user='jcluser', passwd='Juniper!1', port=39001)
dev.open()

rpc = dev.rpc.get_vlan_information({'format':'json'})
showVlan = []
for vlan in rpc['l2ng-l2ald-vlan-instance-information'][0]['l2ng-l2ald-vlan-instance-group']:
    data = {
        'vlan_id': vlan['l2ng-l2rtb-vlan-tag'][0]['data'],
        'name': vlan['l2ng-l2rtb-vlan-name'][0]['data'],
        'status': 'active',
        'interfaces': []
    }
    for intf in vlan['l2ng-l2rtb-vlan-member']:
        data['interfaces'].append(intf['l2ng-l2rtb-vlan-member-interface'][0]['data'])
    showVlan.append(data)
print(showVlan)
