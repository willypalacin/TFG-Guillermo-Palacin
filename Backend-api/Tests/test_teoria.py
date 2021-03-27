from ncclient import manager

device = manager.connect(host='66.129.235.11', port=39000, username='jcluser', password='Juniper!1', hostkey_verify=False, device_params={'name': 'junos'}, allow_agent=False, look_for_keys=False, timeout=3)

netconf_data = '''
    <config>
      <configuration>
        <routing-options operation="replace">
          <router-id>3.3.3.2</router-id>
        </routing-options>
        <routing-options operation="create">
          <static>
            <route>
              <name>0.0.0.0/0</name>
              <next-hop>10.1.0.1</next-hop>
            </route>
          </static>
        </routing-options>
      </configuration>
     </config>
'''

netconf_reply = device.edit_config(target='candidate', config=netconf_data)
print(netconf_reply)
