import json
import pyeapi
import netaddr

data = {
    "Ethernet3": {
        "mode": 'access',
        "vlans": "51"
    }
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
    #commands.append('interface port-channel {}'.format(data['numPortChannel'], 'exit'))
    for intf in data:
        commands.append("interface {}".format(intf))
        commands.append("switchport")
        commands.append("switchport mode {}".format(data[intf]['mode']))
        if "access" in data[intf]['mode']:
            commands.append("switchport access vlan {} ".format(data[intf]['vlans']))
        else:
            commands.append("switchport trunk allowed vlan {} ".format(data[intf]['vlans']))

    createL2int = eapi.run_commands(commands)
except Exception as e:
    print(e)
