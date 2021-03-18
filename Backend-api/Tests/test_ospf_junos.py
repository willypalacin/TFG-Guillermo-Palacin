from ncclient import manager
import jinja2

try:
    data =  {'RouterId': '7.7.7.7', 'ProcessId': '30', 'interfaces': {'ge-0/0/3': '7', 'ge-0/0/9': '8'}}
    device = manager.connect(host='66.129.235.11', port=30000, username='jcluser', password='Juniper!1', hostkey_verify=False, device_params={'name': 'junos'}, allow_agent=False, look_for_keys=False, timeout=3)
    f = open('../Templates/JunosOS/junos_ospf.j2')
    text = f.read()
    template = jinja2.Template(text)
    netconf_data = template.render(rid = data["RouterId"], interfaces=data["interfaces"])
    print(netconf_data)
    netconf_reply = device.edit_config(target='candidate', config=netconf_data)
    device.commit()

except Exception as e:
    print(e)
