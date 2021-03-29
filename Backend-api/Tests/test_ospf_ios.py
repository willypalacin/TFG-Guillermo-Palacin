from netmiko import ConnectHandler
import jinja2, json
import requests
import json
import yaml
import re


try:
    data = {'ospf': {'routerId': '5.5.5.9', 'processId': '4', 'interfaces': {'GigabitEthernet2': {'area': '20', 'coste': '11', 'helloTimer': '22', 'deadTimer': '24', 'priority': '23'}, 'GigabitEthernet3': {}}}}
    url = "https://sandbox-iosxe-latest-1.cisco.com:443/restconf/data/"
    headers = {
      'Accept': 'application/yang-data+json',
      'Content-Type': 'application/yang-data+json',
    }
    f1 = open('../Templates/CiscoIOS/cisco_ospf_interfaces.j2')
    f2 = open('../Templates/CiscoIOS/cisco_ospf_process.j2')

    if data['ospf']['processId']:
        text = f2.read()
        template = jinja2.Template(text)
        config = template.render(pid= int(data['ospf']["processId"]),
                                rid = data['ospf']["routerId"])
        response = requests.put(url + 'Cisco-IOS-XE-native:native/router/Cisco-IOS-XE-ospf:router-ospf/ospf/process-id={}'.format(data['ospf']['processId']),
                                auth=('developer', 'C1sco12345'),
                                headers=headers,
                                data = config, verify=False)
        print (response.text)
    for intf in data['ospf']['interfaces']:
        if data['ospf']['interfaces'][intf]:
            match = re.match(r"([a-z]+)([0-9]+)", intf, re.I)
            if match:
                items = match.groups()
                text = f1.read()
                template = jinja2.Template(text)
                config = template.render(pid= int(data['ospf']["processId"]),
                                            int_name=items[0], int_num=items[1],
                                            hello = data['ospf']['interfaces'][intf]['helloTimer'],
                                            dead = data['ospf']['interfaces'][intf]['deadTimer'],
                                            priority = data['ospf']['interfaces'][intf]['priority'],
                                            cost = int(data['ospf']['interfaces'][intf]['coste']),



                response = requests.put(url + 'Cisco-IOS-XE-native:native/interface/{}={}'.format(items[0], items[1]),
                                        auth=('developer', 'C1sco12345'),
                                        headers=headers,
                                        data = config, verify=False)
                print(response.text)
                if("errors" not in response.text):
                    print("OSPF configurado correctamente")
                else:
                    print(json.loads(response.text)['errors']['error'][0]["error-message"])










    #template = jinja2.Template(text)



    #print(response.text)

except Exception as e:
    print(e)
    print("Hola")
