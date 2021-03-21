
import json
import pyeapi
import netaddr

data = {'ospf': {'routerId': '3.3.3.3', 'processId': '81', 'interfaces': {'Ethernet1': {'area': '20', 'coste': '21', 'helloTimer': '22', 'deadTimer': '24', 'priority': '23'}, 'GigabitEthernet2': {}}}}


eapi_param = pyeapi.connect(
        transport='https',
        host='192.168.1.83',
        username='tfg',
        password='tfg',
        port=443,
        timeout=3
    )
eapi = pyeapi.client.Node(eapi_param)


try:

    response = eapi.run_commands('show ip ospf')
    if response[0]['vrfs']:
        pid= int(list(response[0]['vrfs']['default']['instList'].keys())[0])
        eapi.run_commands(['enable', 'configure', 'no router ospf {}'.format(pid)])
    commands = ['enable', 'configure', 'router ospf {}'.format(data['ospf']['processId']), 'router-id {}'.format(data['ospf']['routerId'])]
    for intf in data['ospf']['interfaces']:
        if data['ospf']['interfaces'][intf]:
            commands.append('interface {}'.format(intf))
            commands.append('ip ospf area {}'.format(data['ospf']['interfaces'][intf]['area']))
            commands.append('ip ospf cost {}'.format(data['ospf']['interfaces'][intf]['coste']))
            commands.append('ip ospf hello-interval {}'.format(data['ospf']['interfaces'][intf]['helloTimer']))
            commands.append('ip ospf dead-interval {}'.format(data['ospf']['interfaces'][intf]['deadTimer']))
            commands.append('ip ospf dead-interval {}'.format(data['ospf']['interfaces'][intf]['priority']))
    ospf_creation = eapi.run_commands(commands)
    #return "El proceso OSPF se ha creado correctamente en {}".format(self.name), 201
#print (ospf_creation)
except Exception as e:
    print(e)
    #return '{}'.format(e), 404
