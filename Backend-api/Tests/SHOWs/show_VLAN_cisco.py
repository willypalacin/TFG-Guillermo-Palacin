from netmiko import ConnectHandler
from ntc_templates.parse import parse_output

c = ConnectHandler(host = '10.10.20.45', username='pepe',
                                 password='pepe',
                                 device_type = 'cisco_ios',
                                 port=22)
c.enable()
vlanShow = c.send_command('show vlan')
vlanShowParsed = parse_output(platform="cisco_ios", command="show vlan", data=vlanShow)
print(vlanShowParsed)
