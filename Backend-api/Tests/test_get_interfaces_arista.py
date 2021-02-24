import requests
import json
import pyeapi
import netaddr


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
    #version_info = eapi.run_commands(['enable', 'configure', 'interface Loopback11', 'ip address 1.2.2.2/24'])
    interfaces = eapi.api('interfaces').getall()
    data = {'interfaces': []}
    for key in interfaces:
        if key != 'defaults':
            data['interfaces'].append(key)

    print (data)

except Exception:
    print("Error")
