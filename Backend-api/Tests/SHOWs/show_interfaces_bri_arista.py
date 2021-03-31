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
    interfaces = eapi.run_commands(['enable', 'show ip interface brief'])[1]['interfaces']

    showInterfaces = {}
    for intf in interfaces:
        showInterfaces[intf] = {
                'adminStatus' : interfaces[intf]['interfaceStatus'],
                'proStatus' : interfaces[intf]['lineProtocolStatus'],
                'ip' : interfaces[intf]['interfaceAddress']['ipAddr']['address'],
            }
    print(showInterfaces)



except Exception:
    print("Error")
