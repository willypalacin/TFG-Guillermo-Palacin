from netmiko import ConnectHandler
import jinja2, json
from ntc_templates.parse import parse_output
import yaml
import requests


c = ConnectHandler(host = 'sandbox-iosxe-latest-1.cisco.com', username='developer',
                                 password='C1sco12345',
                                 device_type = 'cisco_ios',
                                 port=22)
c.enable()


showOspfInt = c.send_command('show ip ospf interface brief')

showOspfIntParsed = parse_output(platform="cisco_ios", command="show ip ospf interface brief", data=showOspfInt)


print (showOspfIntParsed)
