import requests

BASE = "http://127.0.0.1:5000/"

#data = [{"likes": 100, "name": "jose mari", "views": 1000}, {"likes": 98, "name": "Antonio", "views": 1000},{"likes": 75, "name": "Puri", "views": 1000},
#{"likes": 2345, "name": "Jose", "views": 1000}]

data = {"name": "mi Cisco", "type": "cisco_ios", "ip": "ios-xe-mgmt.cisco.com", "usnm":"developer", "pass": "C1sco12345" }

response = requests.put(BASE + "device/{}".format(data["name"]), data)
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
