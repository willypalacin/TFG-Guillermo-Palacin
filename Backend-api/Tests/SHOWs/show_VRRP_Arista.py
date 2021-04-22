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
    showVrrpRun = eapi.run_commands(['enable', 'show vrrp'])[1]
    showVrrp= []
    for vr in showVrrpRun['virtualRouters']:
        data = {
            'interface': vr['interface'],
            'group': vr['groupId'],
            'state': vr['state'],
            'time': vr['skewTime'],
            'master_ip': vr['masterAddr'],
            'group_ip': vr['virtualIp']
        }
        showVrrp.append(data)
    print(showVrrp)
except Exception as e:
    print(e)
