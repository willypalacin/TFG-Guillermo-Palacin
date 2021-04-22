from netmiko import ConnectHandler
import jinja2, json
from ntc_templates.parse import parse_output
import re
import yaml

c = ConnectHandler(host = 'sandbox-iosxe-latest-1.cisco.com', username='developer',
                                 password='C1sco12345',
                                 device_type = 'cisco_ios',
                                 port=22, timeout=10)
c.enable()
vrrpData = c.send_command('show vrrp brief').split("\n")
showVrrp = []
i = 0
for vrrp in vrrpData:
    if i != 0:
        line = re.split("\\s+", vrrp)
        print(line)

        data = {
            'interface': line[0],
            'group': line[1],
            'state': line [5],
            'time': line[3],
            'master_ip': line[6],
            'group_ip': line[7]
        }
        showVrrp.append(data)
    i = i+1

print(showVrrp)
print(yaml.dump(showVrrp))
