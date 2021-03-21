from ncclient import manager, xml_
import xmltodict
from xml.etree import ElementTree as ET
import yaml


device = manager.connect(host='66.129.235.11', port=31000, username='jcluser', password='Juniper!1', hostkey_verify=False, device_params={'name': 'junos'}, allow_agent=False, look_for_keys=False, timeout=3)
netconf_data = """
        <config>
          <configuration>
            <routing-options>
            </routing-options>
          </configuration>
        </config>
    """

    #netconf_reply = device.edit_config(target='candidate', config=netconf_data)
    #device.commit()
data = {'ospf': {'routerId': 'No configurado', 'processId': 'No configurado', 'interfaces': {}}}
get_filter = """
    <configuration>
        <routing-options>
        </routing-options>
        <protocols>
        <ospf>
        </ospf>
        </protocols>
    </configuration>
    """
nc_get_reply = device.get(('subtree', get_filter))
print (nc_get_reply)
dict =  xmltodict.parse(str(nc_get_reply))
if 'router-id' in dict['rpc-reply']['data']['configuration']['routing-options']:
    data['ospf']['routerId'] = dict['rpc-reply']['data']['configuration']['routing-options']['router-id']
    data['ospf']['processId'] = '0'
    for intf in dict['rpc-reply']['data']['configuration']['protocols']['ospf']['area']:
        data['ospf']['interfaces'].update({intf['interface']['name']: {}})
        intName = intf['interface']['name']
        data['ospf']['interfaces'][intName]['area'] = intf['name'].split('.')[3]
        data['ospf']['interfaces'][intName]['helloTimer'] =intf['interface']['hello-interval']
        data['ospf']['interfaces'][intName]['coste'] = intf['interface']['metric']
        data['ospf']['interfaces'][intName]['deadTimer'] = intf['interface']['dead-interval']
        data['ospf']['interfaces'][intName]['priority'] = intf['interface']['priority']

else:
    print("no")
print(yaml.dump(data, default_flow_style=False))






#print(dict['rpc-reply']['data']['configuration']['routing-options']['router-id'])
