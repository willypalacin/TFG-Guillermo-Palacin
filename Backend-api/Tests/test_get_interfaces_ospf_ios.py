import requests
import yaml
import requests
import json


data = {'ospf': {'routerId': 'No configurado', 'processId': 'No configurado', 'interfaces': {}}}

baseUrl = "https://sandbox-iosxe-latest-1.cisco.com:443/restconf/data/"


headers = {
  'Accept': 'application/yang-data+json',
  'Content-Type': 'application/yang-data+json',
  'Authorization': 'Basic Y2lzY286Y2lzY29fMTIzNCE='
}
response = requests.get(baseUrl + "Cisco-IOS-XE-native:native/interface" , auth=('developer', 'C1sco12345'),
                            headers=headers, verify=True)

data = {'ospf': {'routerId': 'No configurado', 'processId': 'No configurado', 'interfaces': {}}}

dataResponse = json.loads(response.text)

rid = []
pid = []

for intf in dataResponse['Cisco-IOS-XE-native:interface']:
    for i in range(0,len(dataResponse['Cisco-IOS-XE-native:interface'][intf])):

        if 'ip' in dataResponse['Cisco-IOS-XE-native:interface'][intf][i].keys():
            if 'Cisco-IOS-XE-ospf:router-ospf' in dataResponse['Cisco-IOS-XE-native:interface'][intf][i]['ip'].keys():
                intName = '{}{}'.format(intf, dataResponse['Cisco-IOS-XE-native:interface'][intf][i]['name'])
                data['ospf']['interfaces'].update({intName : {}})
                dataOspf=dataResponse['Cisco-IOS-XE-native:interface'][intf][i]['ip']['Cisco-IOS-XE-ospf:router-ospf']['ospf']
                print(dataOspf)
                data['ospf']['interfaces'][intName]['area'] = dataOspf['process-id'][0]['area'][0]['area-id']
                if "hello-interval" in dataOspf.keys():
                    data['ospf']['interfaces'][intName]['helloTimer'] = dataOspf['hello-interval']
                if "cost" in dataOspf.keys():
                    data['ospf']['interfaces'][intName]['coste'] = dataOspf['cost']
                if "dead-interval" in dataOspf.keys():
                    data['ospf']['interfaces'][intName]['deadTimer'] = dataOspf['dead-interval']
                if "priority" in dataOspf.keys():
                    data['ospf']['interfaces'][intName]['priority'] = dataOspf['priority']


response = requests.get(baseUrl + "Cisco-IOS-XE-native:native/router/router-ospf" , auth=('developer', 'C1sco12345'),
                            headers=headers, verify=True)
dataResponse = json.loads(response.text)
print(dataResponse)
if 'ospf' in dataResponse['Cisco-IOS-XE-ospf:router-ospf'].keys():
    for process in range(0,len(dataResponse['Cisco-IOS-XE-ospf:router-ospf']['ospf']['process-id'])):
        pid.append(dataResponse['Cisco-IOS-XE-ospf:router-ospf']['ospf']['process-id'][process]['id'])
        rid.append(dataResponse['Cisco-IOS-XE-ospf:router-ospf']['ospf']['process-id'][process]['router-id'])
data['ospf']['routerId'] = str(rid).strip("[]''")
data['ospf']['processId'] = str(pid).strip("[]")
print(yaml.dump(data, default_flow_style=False))
