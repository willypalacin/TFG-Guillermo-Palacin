import requests
import json

BASE = "http://127.0.0.1:5000/"

#data = [{"likes": 100, "name": "jose mari", "views": 1000}, {"likes": 98, "name": "Antonio", "views": 1000},{"likes": 75, "name": "Puri", "views": 1000},
#{"likes": 2345, "name": "Jose", "views": 1000}]

data = {"name": "Router_1", "port":8181,   "type": "cisco_ios", "ip": "ios-xe-mgmt.cisco.com", "usnm":"developer", "pass": "C1sco12345" }

response = requests.put(BASE + "device/Router_1/interface", json.dumps(data))
print(response)



#response = requests.delete(BASE + "video/1000")
#print(response)
#response = requests.delete(BASE + "video/2")
#print(response)
#input()
#print("GETTEANDO\n")
#for i in range (len(data)):
#    response = requests.get(BASE + "video/{}".format(i))
#    print(response.json())
