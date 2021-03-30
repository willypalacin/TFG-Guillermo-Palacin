from netmiko import ConnectHandler
import jinja2, json
import requests
import json
import yaml
import re
import xmltodict

#device = manager.connect(host='66.129.235.11', port=37000, username='jcluser', password='Juniper!1', hostkey_verify=False, device_params={'name': 'junos'}, allow_agent=False, look_for_keys=False, timeout=3)
baseUrl = "https://sandbox-iosxe-latest-1.cisco.com:443/restconf/data/"
f = open('../Templates/CiscoIOS/cisco_vrrp.j2')
data = {
    "vrrp":{
       "GigabitEthernet2":{
          "ipVrrp":"2.2.2.3",
          "preempt":"1",
          "grupo":"20",
          "priority":"20"
       }
    }
}
headers = {
  'Accept': 'application/yang-data+json',
  'Content-Type': 'application/yang-data+json',
}
for intf in data['vrrp']:
    match = re.match(r"([a-z]+)([0-9]+)", intf, re.I)
    if match:
        items = match.groups()
        text = f.read()
        template = jinja2.Template(text)
        config_restconf = template.render(group=data['vrrp'][intf]['grupo'], priority=data['vrrp'][intf]['priority'],
                                 preempt=data['vrrp'][intf]['preempt'], virtual_ip=data['vrrp'][intf]['ipVrrp'])

        print (config_restconf)

        response = requests.put(baseUrl + 'Cisco-IOS-XE-native:native/interface/{}={}/vrrp'.format(items[0], items[1]),
                                auth=('developer', 'C1sco12345'),
                                headers=headers,
                                data = config_restconf, verify=False)
        print(response.text)
