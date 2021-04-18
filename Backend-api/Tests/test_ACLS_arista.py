
import json
import pyeapi
import netaddr

data = {
 'paquillo': {
    "rule": {
        "num": '20',
        "sourceAddr": "3.3.3.0/24",
        "destAddr": '4.4.4.0/24',
        "protocol": 'tcp',
        "destPort": '33',
        "action": 'discard'
    },
    "interfaz": {
        "nombre": 'Ethernet3',
        "apply": "input"
    }

}}


eapi_param = pyeapi.connect(
        transport='https',
        host='192.168.1.84',
        username='tfg',
        password='tfg',
        port=443,
        timeout=3
    )
eapi = pyeapi.client.Node(eapi_param)

commands = ["enable", "configure"]
try:
    tipoAcl = "standard"
    inout = "in"
    string = ""
    for rule in data:
        if data[rule]['rule']['num'] != '':
            if data[rule]['rule']['protocol'] != '' or data[rule]['rule']['destAddr'] != '' or data[rule]['rule']['destPort']!= '':
                tipoAcl = "extended"
            if "accept" in data[rule]['rule']['action']:
                data[rule]['rule']['action']  = "permit"
            if "discard" in data[rule]['rule']['action']:
                data[rule]['rule']['action']  = "deny"
                commands.append("ip access-list {}".format(rule))
                if data[rule]['rule']['protocol'] == '':
                    data[rule]['rule']['protocol'] = 'ip'
                string = '{} {} {} {} {}'.format(data[rule]['rule']['num'], data[rule]['rule']['action'], data[rule]['rule']['protocol'],data[rule]['rule']['sourceAddr'], data[rule]['rule']['destAddr'])
                if "ip" not in  data[rule]['rule']['protocol']:
                    string = string + " eq " +  data[rule]['rule']['destPort']
                commands.append(string)
        if data[rule]['interfaz']['nombre'] != '':
            commands.append("interface {}".format(data[rule]['interfaz']['nombre']))
            if "output" in data[rule]['interfaz']['apply']:
                inout = "out"
            commands.append("ip access-group {} {}".format(rule, inout))


        print(commands)
        createAcl = eapi.run_commands(commands)
        print(createAcl)




    #print (ospf_creation)
except Exception as e:
    print(e)
    #return '{}'.format(e), 404
