#!/usr/bin/env python3.6
import os
import requests
import json

os.environ['NO_PROXY'] = 'pdns-m1.avp.ru'
os.environ['no_proxy'] = 'pdns-m1.avp.ru'
os.environ['no_proxy'] = '127.0.0.1'

#url='http://pdns-m1.avp.ru/api_pdns/api/v1/servers/localhost/zones'

url='http://pdns-m1.avp.ru/api_pdns/api/v1/servers/localhost/zones/trulala.net'
url='http://127.0.0.1:5000/api/v1/servers/localhost/zones/trulala.net'
#url='http://pdns-m1.avp.ru/api_pdns/api/v1/servers/localhost/statistics'
headers = { 'X-API-Key' : 'keykey' }
cert = ('ostest.crt','ostest.key')
rootCA = 'RootCA-cacert.pem'

payload = {
   "rrsets": [
        {
            "name": "api1-ns.trulala.net.",
            "type": "A",
            "ttl": 3600,
            "changetype": "REPLACE",
            "records" : [
                {
                   "content": "5.12.12.12",
                   "disabled": False
               }
           ],
           "comments" :
           [
               { "account": "api",
                  "content": "API add record"
               }
           ]

     }
  ]
}

payloadNS = {
   "rrsets": [
        {
            "name": "2.www.trulala.net.", "type": "NS", "ttl": 300, "changetype": "REPLACE",
            "records" : 
                [
                    {"name" : "2.www.trulala.net.", "type" : "NS", "content": "w1.trulula.net.", "disabled": False, "set-ptr":False },
                    {"name" : "2.www.trulala.net.", "type" : "NS", "content": "w2.trulula.net.", "disabled": False, "set-ptr":False }
               ],
           "comments" :
           [
               { "account": "api",
                 "content": "API add record"
               }
           ]

     }
  ]
}

#req=requests.get(url,headers=headers,cert=cert,verify=rootCA)
req=requests.patch(url,headers=headers,cert=cert,verify=rootCA, data=json.dumps(payload))
#req=requests.patch(url,cert=cert,verify=rootCA, data=json.dumps(payloadNS))
#print (json.dumps(payload))
print(req.status_code)
print(req.text)
#print(req.json())
print(req.headers)
#print(req.json())
#print r.headers['content-type']'
