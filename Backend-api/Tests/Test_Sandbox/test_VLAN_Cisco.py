from netmiko import ConnectHandler
import jinja2, json
import requests
import json
import yaml
import re


try:
    data = {'ospf': {'routerId': '5.5.5.9', 'processId': '4', 'interfaces': {'GigabitEthernet2': {'area': '20', 'coste': '11', 'helloTimer': '22', 'deadTimer': '24', 'priority': '23'}, 'GigabitEthernet3': {}}}}
    url = "https://10.10.20.177:443/restconf/data/"
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
except Exception as e:
    print(e)
    print("Hola")
