from netmiko import ConnectHandler
import jinja2, json
from ntc_templates.parse import parse_output

c = ConnectHandler(host = 'sandbox-iosxe-latest-1.cisco.com', username='developer',
                                 password='C1sco12345',
                                 device_type = 'cisco_ios',
                                 port=22)
c.enable()
interfaces = c.send_command('show ip int brief')

vlan_parsed = parse_output(platform="cisco_ios", command="show ip interface brief", data=interfaces)
showInterfaces = {}
for intf in vlan_parsed:
    showInterfaces[intf['intf']] = {
            'adminStatus' : intf['status'],
            'proStatus' : intf['proto'],
            'ip' : intf['ipaddr'],
        }

print(showInterfaces)
