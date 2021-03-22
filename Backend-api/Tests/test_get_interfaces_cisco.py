import requests
import json
url = "https://sandbox-iosxe-latest-1.cisco.com:443/restconf/data/ietf-interfaces:interfaces"


headers = {
  'Accept': 'application/yang-data+json',
  'Content-Type': 'application/yang-data+json',
  'Authorization': 'Basic Y2lzY286Y2lzY29fMTIzNCE='
}
response = requests.get(url, auth=('developer', 'C1sco12345'),
                            headers=headers, verify=True)

data = {'interfaces': []}

dataResponse = json.loads(response.text)
for intf in dataResponse['ietf-interfaces:interfaces']['interface']:
    data['interfaces'].append(intf['name'])
print(intf)
