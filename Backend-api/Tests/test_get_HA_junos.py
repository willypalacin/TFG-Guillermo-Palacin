from ncclient import manager, xml_
import xmltodict
from xml.etree import ElementTree as ET
import yaml
data = {
    "vrrp":{}

 }
try:
    device = manager.connect(host='66.129.235.11', port=37000, username='jcluser', password='Juniper!1', hostkey_verify=False, device_params={'name': 'junos'}, allow_agent=False, look_for_keys=False, timeout=3)

        #netconf_reply = device.edit_config(target='candidate', config=netconf_data)
        #device.commit()
    res = device.command('show vrrp' , format='json')
    #hola = ET.fromstring(res)
    #data_xml = xmltodict.parse(str(res))
    dict_json = json.dumps(str(res))
    print(dict_json)


    #nombreInterfaz=data_xml['rpc-reply']['vrrp-information']['vrrp-interface']['interface']
    #data['vrrp'].update({nombreInterfaz:{}})
    #print (data_xml['rpc-reply']['vrrp-information']['vrrp-interface']['group'])
    #print(data_xml['rpc-reply']['vrrp-information']['vrrp-interface']['virtual-ip-address'])




    #print(data_xml['rpc-reply']['vrrp-information'].keys())

except:
    data['vrrp'].update({"no configurado":{}})
    print (data)
    print(yaml.dump(data, default_flow_style=False))


 #<interface>ge-0/0/1.0</interface>
    #        <interface-state>down</interface-state>
    #        <group>2</group>
    #        <vrrp-state>init</vrrp-state>
    #        <vrrp-mode>Active</vrrp-mode>
    #        <timer-name>N</timer-name>
    #        <timer-value>0.000</timer-value>
#            <local-interface-address>2.2.2.1</local-interface-address>
#            <virtual-ip-address>2.2.2.5</virtual-ip-address>
