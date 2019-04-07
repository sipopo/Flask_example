from flask import Flask, request, Response
import requests
import json

app = Flask(__name__)

headers = {'X-API-Key': 'keykey'}


@app.route("/api/v1/servers/localhost/zones/<string:zone>", methods=['GET', 'POST'])
def zones(zone):
    url = 'http://192.168.199.100:8081/api/v1/servers/localhost/zones/' + zone
    if request.method == 'GET':
        response = requests.get(url, headers=headers)
        print(zone)
        if zone == 'example.com.':
            status_code = 203
        else:
            status_code = response.status_code
        answer = Response(response.json(), status=status_code, content_type='application/json')

    else:
        answer = Response("I don't want to see you", status=404)
    return answer




if __name__ == '__main__':
    app.run(debug=True)
