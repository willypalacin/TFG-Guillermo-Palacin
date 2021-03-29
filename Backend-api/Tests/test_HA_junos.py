from ncclient import manager, xml_
import xmltodict
import jinja2
from xml.etree import ElementTree as ET

try:
     data = {
        "vrrp":{
           "ge-0/0/1":{
              "ipVrrp":"1.1.1.2",
              "preempt":" ",
              "grupo":"20",
              "priority":"20"
           }
        }
     }
     device = manager.connect(host='66.129.235.11', port=37000, username='jcluser', password='Juniper!1', hostkey_verify=False, device_params={'name': 'junos'}, allow_agent=False, look_for_keys=False, timeout=3)
     f = open('../Templates/JunosOS/junos_vrrp.j2')
     text = f.read()
     intName = list(data['vrrp'].keys())[0]
     get_filter = """
     <configuration>
         <interfaces>

         </interfaces>
     </configuration>
     """
     nc_get_reply = device.get(('subtree', get_filter))
     ip_int = ""
     dict_int = xmltodict.parse(str(nc_get_reply))

     for intf in dict_int['rpc-reply']['data']['configuration']['interfaces']['interface']:
        print(intf['name'])
        if intf['name'] == intName:
            ip_int = intf['unit']['family']['inet']['address']['name']
            template = jinja2.Template(text)
            config_netconf = template.render(int_name=intName, ip_int=ip_int,
                                     group=data['vrrp'][intName]['grupo'], priority=data['vrrp'][intName]['priority'],
                                     preempt=data['vrrp'][intName]['preempt'], virtual_ip=data['vrrp'][intName]['ipVrrp'])

            netconf_reply = device.edit_config(target='candidate', config=config_netconf)

            comit = device.commit()
            print(comit)



except Exception as e:
 print("Necesitas configurar la interfaz primero para activar VRRP")
