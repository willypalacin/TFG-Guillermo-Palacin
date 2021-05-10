import jinja2, json
import requests
import json
import yaml
import re
from ipaddress import IPv4Network

data = {
        "red": '24.24.24.0/24',
        "gw": '10.10.20.254',
        "intf": '',
        "metric": '30'
}

try:
    url = "https://sandbox-iosxe-latest-1.cisco.com:443/restconf/data/"
    headers =  {
      'Accept': 'application/yang-data+json',
      'Content-Type': 'application/yang-data+json',
    }
    f = open('../Templates/CiscoIOS/cisco_static_routing.j2')
    netmask = IPv4Network(data['red']).netmask
    print(netmask)
    text = f.read()
    template = jinja2.Template(text)
    config = template.render(intf=data['intf'],
                             ip=data['red'].split("/")[0],
                             mask=netmask, metric=data['metric'], gw=data['gw'])
    response = requests.put(url + "Cisco-IOS-XE-native:native/ip/route/ip-route-interface-forwarding-list={},{}".format(data['red'].split("/")[0], netmask),
                            auth=("developer", "C1sco12345"),headers=headers, data = config, verify=False)
    print(response.text)


except Exception as e:
    print(e)
    print("Hola")
