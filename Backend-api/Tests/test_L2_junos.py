from ncclient import manager
import jinja2

data = {
    "xe-0/0/1": {
        "mode": 'trunk',
        "vlans": "51,53"
    }

}




try:
    device = manager.connect(host='192.168.1.233', port=830, username='root', password='tfgtfg1', hostkey_verify=False, device_params={'name': 'junos'}, allow_agent=False, look_for_keys=False, timeout=3)
    f = open('../Templates/JunosOS/junos_interfaz_n2.j2')
    text = f.read()
    template = jinja2.Template(text)
    vlans = []
    for intf in data:
        if data[intf]['vlans'] != '':
            if "-" in data[intf]['vlans']:
                aux = vlans.split("-")
                for i in range(int(aux[0]), int(aux[1])):
                    vlans.append(i)
            else:
                if "," in data[intf]['vlans']:
                    vlans = data[intf]['vlans'].split(",")
                    print(str(vlans))
                else:
                    if data[intf]['vlans'] != '':
                        vlans.append(data[intf]['vlans'])

        netconf_data = template.render(intf = intf, mode=data[intf]['mode'], vlans = vlans)
        print(netconf_data)
        netconf_reply = device.edit_config(target='candidate', config=netconf_data)
    device.commit()

except Exception as e:
    print(e)
