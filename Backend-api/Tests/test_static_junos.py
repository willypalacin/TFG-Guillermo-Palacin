from ncclient import manager
import jinja2

data = {
        "red": '24.24.24.0/24',
        "gw": '10.10.20.254',
        "intf": '',
        "metric": '30'
}

try:
    f = open('../Templates/JunosOS/junos_static_routing.j2')
    device = manager.connect(host='66.129.235.11', port=49000, username='jcluser', password='Juniper!1', hostkey_verify=False, device_params={'name': 'junos'}, allow_agent=False, look_for_keys=False, timeout=10)
    text = f.read()
    template = jinja2.Template(text)
    netconf_data = template.render(ip=data['red'], gw = data['gw'], metric=data['metric'])
    print(netconf_data)
    netconf_reply = device.edit_config(target='candidate', config=netconf_data)
    device.commit()

except Exception as e:
    print(e)
