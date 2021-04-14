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
    data = {
    "vlanId": 44,
    "vlanNom": "Paca",
    "layer3": {
        #"ip": "99.99.99.99/24"
    }

    }
    eapi = pyeapi.client.Node(eapi_param)
    commands = ["enable", "configure"]
    if data['vlanId']:
        commands.append("vlan {}".format(data['vlanId']))
        if data['vlanNom']:
            commands.append("name {}".format(data['vlanNom']))
        else:
            commands.append("name Vlan{}".format(data['vlanId']))
    if data['layer3']:
        if data['layer3']['ip']:
            commands.append("interface vlan {}".format(data['vlanId']))
            commands.append("ip address {}".format(data['layer3']['ip']))
            commands.append("no shutdown".format(data['layer3']['ip']))
    vlan = eapi.run_commands(commands)

except Exception as e:
    print(e)
