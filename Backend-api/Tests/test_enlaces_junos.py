from ncclient import manager
import jinja2

data = {
    "numPortChannel": 67,
    "mode": "active",
    "interfaces": ["em2"]
}


try:
    device = manager.connect(host='192.168.1.233', port=830, username='root', password='tfgtfg1', hostkey_verify=False, device_params={'name': 'junos'}, allow_agent=False, look_for_keys=False, timeout=3)
    f = open('../Templates/JunosOS/junos_port_channel.j2')
    text = f.read()
    template = jinja2.Template(text)
    vlans = []
    netconf_data = template.render(num_pc = data['numPortChannel'], mode=data['mode'], interfaces=data['interfaces'])
    print(netconf_data)
    netconf_reply = device.edit_config(target='candidate', config=netconf_data)
    device.commit()

except Exception as e:
    print(e)
