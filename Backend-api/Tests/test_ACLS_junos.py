from ncclient import manager
import jinja2

data = {
 'loles': {
    "rule": {
        "num": '10',
        "sourceAddr": "1.1.1.0/24",
        "destAddr": '',
        "protocol": 'tcp',
        "destPort": '332',
        "action": 'accept'
    },
    "interfaz": {
        "nombre": "ge-0/0/3",
        "apply": "input"
    }

}}



try:
    device = manager.connect(host='66.129.235.12', port=35000, username='jcluser', password='Juniper!1', hostkey_verify=False, device_params={'name': 'junos'}, allow_agent=False, look_for_keys=False, timeout=3)
    f = open('../Templates/JunosOS/junos_acl.j2')
    text = f.read()
    template = jinja2.Template(text)
    for rule in data:
        netconf_data = template.render(nombre_acl = rule,
                                       num=data[rule]['rule']['num'],
                                       sa=data[rule]['rule']['sourceAddr'],
                                       da=data[rule]['rule']['destAddr'],
                                       protocol=data[rule]['rule']['protocol'],
                                       action = data[rule]['rule']['action'],
                                       dest_port=data[rule]['rule']['destPort'],
                                       intf= data[rule]['interfaz']['nombre'],
                                       inout=data[rule]['interfaz']['apply'])
        print(netconf_data)
        netconf_reply = device.edit_config(target='candidate', config=netconf_data)
        device.commit()

except Exception as e:
    print(e)
    netconf_reply = device.rollback(rollback=0)
    device.commit()
