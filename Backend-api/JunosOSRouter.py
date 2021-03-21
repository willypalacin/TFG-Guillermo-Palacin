from Device import Device
from ncclient import manager
import jinja2, json
from netaddr import IPAddress
import xmltodict
import yaml

class JunosOSRouter(Device):
    def __init__(self, name, ip, type, username, password, port):
        Device.__init__(self, name, ip, type, username, password, port)


    def checkConnectivity(self):
        try:
            connection = manager.connect(host=self.ip, port=int(self.port),
                                     username=self.username, password=self.password, hostkey_verify=False,
                                     device_params={'name': 'junos'}, allow_agent=False,
                                     look_for_keys=False, timeout=3)

            self.connection = connection
            print("HOLA")
            return 201, "Dispositivo {} anadido satisfactoriamente".format(self.name)
        except:
            return 404, "No se ha encontrado ningun dispositivo con IP {}".format(self.ip)

    def editInterface(self, int_name, desc, ip, mask):
        maskBits = IPAddress(mask).netmask_bits()
        f = open('Templates/JunosOS/junos_interface.j2')
        text = f.read()
        template = jinja2.Template(text)
        config_netconf = template.render(int_name=int_name, ip=ip,
                                 mask=maskBits, description=desc)


        try:
            netconf_reply = self.connection.edit_config(target='candidate', config=config_netconf)
            print(netconf_reply)
            self.connection.commit()
            return 201
        except:
            return 404

    def getInterfacesList(self):
        try:
            data = {'interfaces': []}
            res = self.connection.command('show interfaces ge-0/0/* terse' , format='xml')
            #hola = ET.fromstring(res)
            data_xml = xmltodict.parse(str(res))

            for key in data_xml['rpc-reply']['interface-information']['physical-interface']:
                data['interfaces'].append(key['name'])

            return json.dumps(data), 201
        except:
            return {}, 404


    def getOspfData(self):
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
        try:
            nc_get_reply = self.connection.get(('subtree', get_filter))
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

            return yaml.dump(data, default_flow_style=False), 201
        except Exception as e:
            return yaml.dump(data, default_flow_style=False), 404




    def createOspf(self, data):
        try:
            f = open('Templates/JunosOS/junos_ospf.j2')
            text = f.read()
            template = jinja2.Template(text)
            netconf_data = template.render(rid = data['ospf']["routerId"], interfaces=data['ospf']["interfaces"])
            print(netconf_data)
            netconf_reply = self.connection.edit_config(target='candidate', config=netconf_data)
            self.connection.commit()
            return 'OSPF Configurado correctamente en {}'.format(self.name), 201
        except Exception as e:
            return '{}'.format(e), 404
