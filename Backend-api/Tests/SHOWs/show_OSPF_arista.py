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
    showOspfRun = eapi.run_commands(['enable', 'show ip ospf interface brief'])[1]
    showOspf= []


    for instance in showOspfRun['vrfs']['default']['instList']:
        for intf in showOspfRun['vrfs']['default']['instList'][instance]['interfaces']:
            data = {
                'interface': intf,
                'area': showOspfRun['vrfs']['default']['instList'][instance]['interfaces'][intf]['area'],
                'ip_address_mask': showOspfRun['vrfs']['default']['instList'][instance]['interfaces'][intf]['interfaceAddress'],
                'cost': showOspfRun['vrfs']['default']['instList'][instance]['interfaces'][intf]['cost'],
                'state': showOspfRun['vrfs']['default']['instList'][instance]['interfaces'][intf]['state'],
                'neighbors_fc': '0/0'
            }
            showOspf.append(data)
except Exception as e:
    print(e)
