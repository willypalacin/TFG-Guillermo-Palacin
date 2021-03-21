import json
import pyeapi
import netaddr
import yaml

data = {'ospf': {'routerId': 'No configurado', 'processId': 'No configurado', 'interfaces': {}}}


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
        data['ospf']['processId'] = str((list(response[0]['vrfs']['default']['instList'].keys())[0]))
        data['ospf']['routerId']= response[0]['vrfs']['default']['instList'][data['ospf']['processId']]['routerId']
        response = eapi.run_commands('show ip ospf interface')
        #if response[0]['vrfs']:
        #data['ospf']['interfaces'].update({self.currentInterface: {}})
        for intf in response[0]['vrfs']['default']['instList'][data['ospf']['processId']]['interfaces']:
            dataInterfaz= response[0]['vrfs']['default']['instList'][data['ospf']['processId']]['interfaces'][intf]
            data['ospf']['interfaces'].update({intf: {}})
            data['ospf']['interfaces'][intf]['ip'] = dataInterfaz['interfaceAddress']
            data['ospf']['interfaces'][intf]['mask'] = dataInterfaz['interfaceMask']
            data['ospf']['interfaces'][intf]['coste'] = dataInterfaz['cost']
            data['ospf']['interfaces'][intf]['priority'] = dataInterfaz['priority']
            data['ospf']['interfaces'][intf]['deadTimer'] = dataInterfaz['helloInterval']
            data['ospf']['interfaces'][intf]['helloTimer'] = dataInterfaz['deadInterval']
            data['ospf']['interfaces'][intf]['area'] = dataInterfaz['area']



    print(yaml.dump(data, default_flow_style=False))
            #data['ospf']['routerId']= response[0]['vrfs']['default']['instList'][str(pid)]



except Exception as e:
    print(e)
