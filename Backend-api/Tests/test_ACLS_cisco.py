from netmiko import ConnectHandler
import jinja2, json
import requests
import json
import yaml
import re
import xmltodict
from ipaddress import IPv4Network
from ipaddress import IPv4Address

data = {
 'Manolete': {
    "rule": {
        "num": '20',
        "sourceAddr": "3.3.3.0/24",
        "destAddr": '',
        "protocol": '',
        "destPort": '',
        "action": 'deny'
    },
    "interfaz": {
        "nombre": '',
        "apply": "input"
    }

}}

baseUrl = "https://sandbox-iosxe-latest-1.cisco.com:443/restconf/data/"
f = open('../Templates/CiscoIOS/cisco_acl.j2')
text = f.read()
template = jinja2.Template(text)

f2 = open('../Templates/CiscoIOS/cisco_acl_interface.j2')
text = f2.read()
template2 = jinja2.Template(text)

headers = {
  'Accept': 'application/yang-data+json',
  'Content-Type': 'application/yang-data+json',
}
tipoAcl = "standard"
inout = "in"
for rule in data:
    if data[rule]['rule']['num'] != '':
        if data[rule]['rule']['protocol'] != '' or data[rule]['rule']['destAddr'] != '' or data[rule]['rule']['destPort']!= '':
            tipoAcl = "extended"
        if "accept" in data[rule]['rule']['action']:
            data[rule]['rule']['action']  = "permit"
        if "discard" in data[rule]['rule']['action']:
            data[rule]['rule']['action']  = "deny"


        netmaskSa = IPv4Network(data[rule]['rule']['sourceAddr']).netmask
        wildcardSa = (str(IPv4Address(int(IPv4Address(netmaskSa))^(2**32-1))))
        netmaskDa = IPv4Network(data[rule]['rule']['sourceAddr']).netmask
        wildcardDa = (str(IPv4Address(int(IPv4Address(netmaskDa))^(2**32-1))))
        restconfDataAcl = template.render(wildcard_sa = wildcardSa,
                                       wildcard_da=wildcardDa,
                                       tipo_acl = tipoAcl,
                                       nombre_acl = rule,
                                       num=data[rule]['rule']['num'],
                                       sa=data[rule]['rule']['sourceAddr'].split("/")[0],
                                       da=data[rule]['rule']['destAddr'].split("/")[0],
                                       protocol=data[rule]['rule']['protocol'],
                                       action = data[rule]['rule']['action'],
                                       dest_port=data[rule]['rule']['destPort'])
        response = requests.patch(baseUrl + 'Cisco-IOS-XE-native:native/ip/access-list',
                                auth=("developer", "C1sco12345"),
                                headers=headers,
                                data = restconfDataAcl, verify=False)
        print(restconfDataAcl)

    if "output" in data[rule]['interfaz']['apply']:
        inout = "out"
    if data[rule]['interfaz']['nombre']:
        match = re.match(r"([a-z]+)([0-9]+)", data[rule]['interfaz']['nombre'], re.I)
        if match:
            items = match.groups()

            restconfDataAclInt = template2.render(inout = inout, nombre_acl = rule)
            print(restconfDataAclInt)
            response = requests.put(baseUrl + 'Cisco-IOS-XE-native:native/interface/{}={}/ip/access-group'.format(items[0], items[1]),
                                    auth=("developer", "C1sco12345"),
                                    headers=headers,
                                    data = restconfDataAclInt, verify=False)
            print(response.text)




print (tipoAcl)
