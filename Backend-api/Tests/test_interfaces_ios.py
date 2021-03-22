import requests
import json
import jinja2
url = "https://sandbox-iosxe-latest-1.cisco.com:443/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet2"


headers = {
  'Accept': 'application/yang-data+json',
  'Content-Type': 'application/yang-data+json',
  'Authorization': 'Basic Y2lzY286Y2lzY29fMTIzNCE='
}


data = {'interfaces': []}

#dataResponse = json.loads(response.text)
f = open('../Templates/CiscoIOS/cisco_interfaces.j2')
text = f.read()
template = jinja2.Template(text)
config = template.render(int_name="GigabitEthernet2",
                         ip="2.2.2.2",
                         mask="255.255.255.0", description="Hola")
print ("CONFIG: \n: {}".format(config))
response = requests.put(url, auth=('developer', 'C1sco12345') ,headers=headers, data = config, verify=False)
if response.text == '':
    print("si")
else:
    print("-{}-".format(response.text))
