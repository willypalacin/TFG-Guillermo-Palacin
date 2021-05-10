from netmiko import ConnectHandler
import jinja2, json
import requests
import json
import yaml
import re


try:
    data = {'ospf': {'routerId': '5.4.4.4', 'processId': '3','default-originate':'1' ,'interfaces': {'GigabitEthernet2': {'area': '20', 'coste': '', 'helloTimer': '', 'deadTimer': '', 'priority': ''}, 'GigabitEthernet3': {}}}}
    url = "https://192.168.1.109:443/restconf/data/"
    headers = {
      'Accept': 'application/yang-data+json',
      'Content-Type': 'application/yang-data+json',
    }
    f1 = open('../Templates/CiscoIOS/cisco_ospf_interfaces.j2')
    f2 = open('../Templates/CiscoIOS/cisco_ospf_process.j2')

    if data['ospf']['processId']:
        text = f2.read()
        template = jinja2.Template(text)
        config = template.render(pid= data['ospf']["processId"],
                                 rid = data['ospf']["routerId"], default_info=data['ospf']['default-originate'])
        response = requests.put(url + 'Cisco-IOS-XE-native:native/router',
                                auth=('cisco', 'cisco'),
                                headers=headers,
                                data = config, verify=False)
        print(config)
        print (response.text)


except Exception as e:
    print(e)
    print("Hola")
