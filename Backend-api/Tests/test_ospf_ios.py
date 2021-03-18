from netmiko import ConnectHandler
import jinja2, json
try:
    data =  {'RouterId': '3.3.3.3', 'ProcessId': '30', 'interfaces': {'GigabitEthernet3': '0', 'GigabitEthernet2': '5'}}
    connection = ConnectHandler(host = 'ios-xe-mgmt.cisco.com', username='developer',
                                password='C1sco12345',
                                device_type = 'cisco_ios',
                                port=8181)
    connection.enable()
    f = open('../Templates/CiscoIOS/cisco_ospf.j2')
    text = f.read()
    template = jinja2.Template(text)
    config = template.render(pid= data['ProcessId'],
                             rid=data['RouterId'],
                             interfaces=data['interfaces']).split('\n')

    output = connection.send_config_set(config)
    start = output.find("%")
    substring = output[start:start+45]
    print(substring)

except Exception as e:
    print(e)
