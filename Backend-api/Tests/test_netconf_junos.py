from ncclient import manager

try:
    device = manager.connect(host='66.129.235.11', port=43000, username='jcluser', password='Juniper!1', hostkey_verify=False, device_params={'name': 'junos'}, allow_agent=False, look_for_keys=False, timeout=3)
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

    netconf_reply = device.edit_config(target='candidate', config=netconf_data)
    device.commit()

    get_filter = """
    <configuration>
      <interfaces>
      </interfaces>
    </configuration>
    """


    nc_get_reply = device.get(('subtree', get_filter))
    print(nc_get_reply)
except:
    print("Hola")
