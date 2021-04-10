import requests
import json
import pyeapi
import netaddr
import re

import datetime

try:
    eapi_param = pyeapi.connect(
        transport='https',
        host='192.168.1.83',
        username='tfg',
        password='tfg',
        port=443,
        timeout=3
    )
    showOspfNeigh = []
    eapi = pyeapi.client.Node(eapi_param)
    ospfNeigh = eapi.run_commands(['enable', 'show ip ospf neighbor'])[1]
    for neigh in ospfNeigh['vrfs']['default']['instList']:
        for entry in ospfNeigh['vrfs']['default']['instList'][neigh]['ospfNeighborEntries']:
            data = {'neighbor_id': entry['routerId'],
                    'priority': entry['priority'],
                    'state': '{}/{}'.format(entry['adjacencyState'].upper(), entry['drState']),
                    'dead_time': datetime.datetime.fromtimestamp(entry['inactivity']).strftime('%S'),
                    'address': entry['interfaceAddress'],
                    'interface': entry['interfaceName']
            }
            showOspfNeigh.append(data)

    print(showOspfNeigh)

### [{'neighbor_id': '172.16.252.25', 'priority': '1', 'state': 'FULL/BDR', 'dead_time': '00:00:39', 'address': '172.16.252.17', 'interface': 'GigabitEthernet6'}]
###














except Exception as e:
    print(e)
