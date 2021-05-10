from netmiko import ConnectHandler
import jinja2, json
import requests
import json
import yaml
import re


data = {'ospf': {'routerId': 'No configurado', 'processId': 'No configurado', 'interfaces': {}}}
try:
    headers = {
      'Accept': 'application/yang-data+json',
      'Content-Type': 'application/yang-data+json',
    }
    baseUrl = "https://192.168.1.109:443/restconf/data/"
    response = requests.get(baseUrl + "Cisco-IOS-XE-native:native/interface" , auth=('cisco', 'cisco'),
                                headers=headers, verify=False)


    dataResponse = json.loads(response.text)

    rid = []
    pid = []
    for intf in dataResponse['Cisco-IOS-XE-native:interface']:
        for i in range(0,len(dataResponse['Cisco-IOS-XE-native:interface'][intf])):
            if 'ip' in dataResponse['Cisco-IOS-XE-native:interface'][intf][i].keys():
                print(dataResponse['Cisco-IOS-XE-native:interface'][intf][i]['ip'].keys())
                if 'Cisco-IOS-XE-ospf:ospf' in dataResponse['Cisco-IOS-XE-native:interface'][intf][i]['ip'].keys():
                    intName = '{}{}'.format(intf, dataResponse['Cisco-IOS-XE-native:interface'][intf][i]['name'])
                    data['ospf']['interfaces'].update({intName : {}})
                    dataOspf=dataResponse['Cisco-IOS-XE-native:interface'][intf][i]['ip']['Cisco-IOS-XE-ospf:ospf']
                    print("DataOSPF")
                    print(dataOspf.keys())
                    data['ospf']['interfaces'][intName]['area'] = dataOspf['process-id'][0]['area']
                    if "hello-interval" in dataOspf.keys():
                        data['ospf']['interfaces'][intName]['helloTimer'] = dataOspf['hello-interval']
                        print(dataOspf['process-id'][0]['area'])
                    if "cost" in dataOspf.keys():
                        data['ospf']['interfaces'][intName]['coste'] = dataOspf['cost']
                    if "dead-interval" in dataOspf.keys():
                        data['ospf']['interfaces'][intName]['deadTimer'] = dataOspf['dead-interval']['value']
                    if "priority" in dataOspf.keys():
                        data['ospf']['interfaces'][intName]['priority'] = dataOspf['priority']
                    print(data)

    response = requests.get(baseUrl + "Cisco-IOS-XE-native:native/router/ospf" , auth=('cisco', 'cisco'),
                                headers=headers, verify=False)
    dataResponse = json.loads(response.text)
    print(response.text)
    print(dataResponse['Cisco-IOS-XE-ospf:ospf'])

    for process in range(0,len(dataResponse['Cisco-IOS-XE-ospf:ospf'])):
        print("entra")
        pid.append(dataResponse['Cisco-IOS-XE-ospf:ospf'][process]['id'])
        rid.append(dataResponse['Cisco-IOS-XE-ospf:ospf'][process]['router-id'])
    data['ospf']['routerId'] = str(rid).strip("[]''")
    data['ospf']['processId'] = str(pid).strip("[]")

    print(yaml.dump(data, default_flow_style=False))

            #data['ospf']['routerId']= response[0]['vrfs']['default']['instList'][str(pid)]
except Exception as e:
    print(yaml.dump(data, default_flow_style=False))
