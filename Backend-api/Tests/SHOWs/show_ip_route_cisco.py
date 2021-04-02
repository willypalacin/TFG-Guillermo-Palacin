from netmiko import ConnectHandler
import jinja2, json
from ntc_templates.parse import parse_output

c = ConnectHandler(host = 'sandbox-iosxe-latest-1.cisco.com', username='developer',
                                 password='C1sco12345',
                                 device_type = 'cisco_ios',
                                 port=22)
c.enable()
interfaces = c.send_command('show ip route')

ipRoute = parse_output(platform="cisco_ios", command="show ip route", data=interfaces)

showIpRoute = []
for route in ipRoute:
    data =  {
            'protocolo' : route['protocol'],
            'red' : route['network'] + "/"+ route['mask'],
            'distancia': route['distance'],
            'metrica': route['metric'],
            'gateway': route['nexthop_ip'],
            'gateway_if': route['nexthop_if']
        }
    showIpRoute.append(data)

print(showIpRoute)
