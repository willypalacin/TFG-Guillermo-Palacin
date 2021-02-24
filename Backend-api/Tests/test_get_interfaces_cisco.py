from netmiko import ConnectHandler
import jinja2, json


connection = ConnectHandler(host = 'ios-xe-mgmt.cisco.com', username='developer',
                            password='C1sco12345',
                            device_type = 'cisco_ios',
                            port=8181)
connection.enable()
output = connection.send_command('show ip interface brief').split('\n')
data = {'interfaces': []}
for i in range (2, len(output)):
    data['interfaces'].append(output[i].split(" ")[0])
