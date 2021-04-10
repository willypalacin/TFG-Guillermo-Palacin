from netmiko import ConnectHandler
import jinja2, json
from ntc_templates.parse import parse_output


c = ConnectHandler(host = '10.10.20.176', username='cisco',
                                 password='cisco',
                                 device_type = 'cisco_ios',
                                 port=22)
c.enable()
ospfNeigh = c.send_command('show ip ospf neighbor')
ospfNeighParsed = parse_output(platform="cisco_ios", command="show ip ospf neighbor", data=ospfNeigh)
print(ospfNeighParsed)



#output
### [{'neighbor_id': '172.16.252.25', 'priority': '1', 'state': 'FULL/BDR', 'dead_time': '00:00:39', 'address': '172.16.252.17', 'interface': 'GigabitEthernet6'}]
###
