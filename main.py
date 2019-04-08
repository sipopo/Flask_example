from flask import Flask, request, Response
from flask import jsonify
import requests
import json

#
import os
os.environ['no_proxy'] = '10.68.70.19'
#

app = Flask(__name__)

# set config settings
with open('config.json', 'r') as f:
    config = json.load(f)

headers = {'X-API-Key': config['DEFAULT'][0]['X-API-Key']}
pdns_url = config['DEFAULT'][0]['PDNS_URL']

message_403 = {"error": "You are not authorized to do it."}
message_500 = {"error": "Something wrong"}

@app.route("/api/v1/servers/localhost/zones/<string:zone>", methods=['GET', 'PATCH'])
def zones(zone):
    url = pdns_url + request.path
    if request.method == 'GET':
        res = requests.get(url, headers=headers)
        
        # Make right answer
        answer = jsonify(res.text)
        answer.status_code = res.status_code
        #answer.headers = res.headers

    else:
        deny = False
        data = json.loads(request.data)
        for rrset in data['rrsets']:
            print(rrset['type'] + " " + rrset['name'])
            if rrset['type'] == 'NS' :
                deny = True
        print("Do not make a request: " + str(deny))
        if not deny:
            res = requests.patch(url, headers=headers, data=json.dumps(data))
            answer = jsonify(res.text)
            answer.status_code = res.status_code
            #answer.headers = res.headers
        else:
            answer = jsonify(message_403)
            answer.status_code = 403

    return answer


if __name__ == '__main__':
    app.run(debug=True)
