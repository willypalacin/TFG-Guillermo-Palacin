import json
import pyeapi
import netaddr
try:
    data = {
        "vrrp":{
           "Ethernet1":{
              "ipVrrp":"1.1.1.2",
              "preempt":"1",
              "grupo":"20",
              "priority":"20"
           }
        }
    }

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
    for intf in data['vrrp']:
      commands.append("interface {}".format(intf))
      commands.append("vrrp {} priority-level {}".format(data['vrrp'][intf]['grupo'], data['vrrp'][intf]['priority']))
      commands.append("vrrp {} ipv4 {}".format(data['vrrp'][intf]['grupo'], data['vrrp'][intf]['ipVrrp']))
      if data['vrrp'][intf]['preempt'] != "0":
           commands.append("vrrp {} {}".format(data['vrrp'][intf]['grupo'], 'preempt'))
      creationVrrp = eapi.run_commands(commands)
      print(creationVrrp)

except Exception as e:

    print(e)
