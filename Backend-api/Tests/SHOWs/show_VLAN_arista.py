import requests
import json
import pyeapi
import netaddr
import re

import datetime

try:
    eapi_param = pyeapi.connect(
        transport='https',
        host='192.168.1.84',
        username='tfg',
        password='tfg',
        port=443,
        timeout=3
    )
    eapi = pyeapi.client.Node(eapi_param)
    vlanShow = eapi.run_commands(['enable', 'show vlan'])[1]
    showVlan = []
    for vlan in vlanShow['vlans']:
        data = {
            'vlan_id': vlan,
            'name': vlanShow['vlans'][vlan]['name'],
            'status': vlanShow['vlans'][vlan]['status'],
            'interfaces': []
        }
        for intf in vlanShow['vlans'][vlan]['interfaces']:
            data['interfaces'].append(intf)
        showVlan.append(data)
    print(showVlan)
except Exception as e:
    print(e)


    #[{'vlan_id': '1', 'name': 'default', 'status': 'active', 'interfaces': ['Gi0/0', 'Gi0/3']}, {'vlan_id': '34', 'name': 'VLAN0034', 'status': 'active', 'interfaces': []}, {'vlan_id': '35', 'name': 'JOSE', 'status': 'MARi', 'interfaces': ['active']}, {'vlan_id': '88', 'name': 'MKTNG', 'status': 'active', 'interfaces': ['Gi0/2']}, {'vlan_id': '1002', 'name': 'fddi-default', 'status': 'act/unsup', 'interfaces': []}, {'vlan_id': '1003', 'name': 'token-ring-default', 'status': 'act/unsup', 'interfaces': []}, {'vlan_id': '1004', 'name': 'fddinet-default', 'status': 'act/unsup', 'interfaces': []}, {'vlan_id': '1005', 'name': 'trnet-default', 'status': 'act/unsup', 'interfaces': []}]
