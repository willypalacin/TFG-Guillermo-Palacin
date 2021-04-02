import requests
import json
import pyeapi
import netaddr
import re



try:
    eapi_param = pyeapi.connect(
        transport='https',
        host='192.168.1.85',
        username='tfg',
        password='tfg',
        port=443,
        timeout=3
    )
    eapi = pyeapi.client.Node(eapi_param)
    ipRoutes = eapi.run_commands(['enable', 'show ip route'])[1]

    showIpRoute = []

    for route in ipRoutes['vrfs']['default']['routes']:
        data = {}
        for via in ipRoutes['vrfs']['default']['routes'][route]['vias']:
            data['protocolo'] = ipRoutes['vrfs']['default']['routes'][route]['routeType']
            data['gateway_if'] = via['interface']
            if 'nexthopAddr' in via.keys():
                data['gateway'] = via['nexthopAddr']
            else:
                data['dateway'] = ''
            data['red'] = route
            if 'preference' in ipRoutes['vrfs']['default']['routes'][route].keys():
                data['distancia'] = ipRoutes['vrfs']['default']['routes'][route]['preference']
            else:
                data['distancia'] = ''
            if 'metric' in ipRoutes['vrfs']['default']['routes'][route].keys():
                data['metrica'] =  ipRoutes['vrfs']['default']['routes'][route]['metric']

            showIpRoute.append(data)

    print(showIpRoute)















except Exception as e:
    print(e)
