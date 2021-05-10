import json
import pyeapi
import netaddr

data = {
        "red": '24.24.24.0/24',
        "gw": '192.168.1.35',
        "intf": '',
        "metric": '30'
}

eapi_param = pyeapi.connect(
        transport='https',
        host='192.168.1.33',
        username='tfg',
        password='tfg',
        port=443,
        timeout=3
    )
eapi = pyeapi.client.Node(eapi_param)

try:
    commands = ["enable", "configure"]
    string = ""
    if data['intf']:
        if data['metric']:
            string = "ip route {} {} metric {}".format(data['red'], data['intf'] , data['metric'])
        else:
            string = "ip route {} {}".format(data['red'], data['intf'])
    else:
        if data['gw']:
            if data['metric']:
                string = "ip route {} {} metric {}".format(data['red'], data['gw'] , data['metric'])
            else:
                string = "ip route {} {}".format(data['red'], data['gw'])
    commands.append(string)
    response = eapi.run_commands(commands)
    #return "El proceso OSPF se ha creado correctamente en {}".format(self.name), 201
#print (ospf_creation)
except Exception as e:
    print(e)
    #return '{}'.format(e), 404
