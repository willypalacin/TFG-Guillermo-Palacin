
import json
import pyeapi
import netaddr

data = {'RouterId': '4.4.4.4', 'ProcessId': '4', 'interfaces': {'Ethernet2': '0', 'Ethernet3': '0'}}

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


    commands = ['enable', 'configure', 'router ospf {}'.format(data['ProcessId']), 'router-id {}'.format(data['RouterId'])]
    for intf in data['interfaces']:
        commands.append('interface {}'.format(intf))
        commands.append('ip ospf area {}'.format(data['interfaces'][intf]))
    ospf_creation = eapi.run_commands(commands)

except Exception as e:
    print(e)
