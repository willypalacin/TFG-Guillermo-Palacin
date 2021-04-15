from ncclient import manager, xml_
import xmltodict
from xml.etree import ElementTree as ET

try:
    device = manager.connect(host='192.168.1.233', port=830, username='root', password='tfgtfg1', hostkey_verify=False, device_params={'name': 'junos'}, allow_agent=False, look_for_keys=False, timeout=3)
    netconf_data = """
        <config>
          <configuration>
            <interfaces>
              <interface>
                <name>ge-0/0/1</name>
                <unit>
                  <name>0</name>
                  <family>
                    <inet>
                      <address>
                        <name>10.0.0.21/24</name>
                      </address>
                    </inet>
                  </family>
                </unit>
              </interface>
            </interfaces>
          </configuration>
        </config>
    """

    #netconf_reply = device.edit_config(target='candidate', config=netconf_data)
    #device.commit()

    get_filter = """
    <configuration>
        <interfaces>
        </interfaces>
    </configuration>
    """
    nc_get_reply = device.get(('subtree', get_filter))
    print(nc_get_reply)
    data = {'interfaces': []}
    #########res = device.command('show interfaces ge-0/0/* terse' , format='xml')
    #hola = ET.fromstring(res)
    ####data_xml = xmltodict.parse(str(res))

    ###for key in data_xml['rpc-reply']['interface-information']['physical-interface']:
        ###print (key['name'])


    #json_d = json.loads(hola.text)
    #print(json_d)




    #print(nc_get_reply)
    #data = xmltodict.parse(str(nc_get_reply))
    #for intf in data['rpc-reply']['data']['configuration']['interfaces']['interface']
    #data['interfaces'].append(intf['name'])
    print(data)


except:
    print("Hola")
