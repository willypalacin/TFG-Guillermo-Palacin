import json
import pyeapi
import netaddr

data = {
    "numPortChannel": 67,
    "mode": "active",
    "interfaces": ["Ethernet2", "Ethernet3"]
}
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

    commands = ['enable', 'configure']
    commands.append('interface port-channel {}'.format(data['numPortChannel'], 'exit'))
    for intf in data['interfaces']:
        commands.append("interface {}".format(intf))
        commands.append("channel-group {} mode {}".format(data['numPortChannel'], data['mode']))
        commands.append("exit")
    createPortChannel = eapi.run_commands(commands)
except Exception as e:
    print(e)
