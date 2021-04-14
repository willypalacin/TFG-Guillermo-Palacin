from ncclient import manager
import jinja2

data = {
    "vlanId": 64,
    "vlanNom": "Paquita",
    "layer3": {
        "ip": "101.101.101.101/24"
} }
try:
    device = manager.connect(host='192.168.1.233', port=830, username='root', password='tfgtfg1', hostkey_verify=False, device_params={'name': 'junos'}, allow_agent=False, look_for_keys=False, timeout=3)
    f = open('../Templates/JunosOS/junos_vlan_interface.j2')
    text = f.read()
    template = jinja2.Template(text)
    netconf_data = template.render(vlan_id = data['vlanId'], vlan_name=data['vlanNom'], ip= data['layer3']['ip'])
    print (netconf_data)
    #print(netconf_data)
    netconf_reply = device.edit_config(target='candidate', config=netconf_data)
    device.commit()

except Exception as e:
    print(e)
