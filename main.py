from flask import Flask, request, Response
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
import json
import logging
import logging.config

#
import os
os.environ['no_proxy'] = '10.68.70.19'
#

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class Access(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(20), nullable=False, default="*") 
    zone = db.Column(db.String(255), nullable=False, default="*")
    record = db.Column(db.String(255), nullable=False, default="*")
    mode = db.Column(db.String(10), nullable=False, default="deny")


# set config settings
with open('config.json', 'r') as f:
    config = json.load(f)

headers = {'X-API-Key': config['DEFAULT'][0]['X-API-Key']}
pdns_url = config['DEFAULT'][0]['PDNS_URL']

# --- config for loggin
dc = config['DEFAULT'][0]['logging'][0]
logger = logging.config.dictConfig(dc)
#logger = logging.getLogger('main')
#logger.setLevel(logging.DEBUG)
#
#ch = logging.StreamHandler()
#ch.setLevel(logging.DEBUG)
#
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#
#ch.setFormatter(formatter)
#
#logger.addHandler(ch)
# --- End config for logging

message_403 = {"error": "You are not authorized to do it."}
message_500 = {"error": "Something wrong"}

@app.route("/api/v1/servers/localhost/zones/<string:zone>", methods=['GET', 'PATCH'])
def zones(zone):
    # check rights for login - todo
    # get_login from header
    try:
        login = request.headers['X-Login-Id']
    except:
        login = "no-body"
        app.logger.error("I don't found login in header")

    try:
        # check rignts to zone
        app.logger.debug('checking rights for user %s to zone %s', login, zone)
        query = Access.query.filter_by(login=login, zone=zone, mode='allow').all()
        if len(query) == 0 :
            app.logger.info("login %s doesn't have allowing records in database for zone %s ", login ,zone )
            answer = jsonify(message_403)
            answer.status_code = 403
            return answer
    except Exception as ex:
            app.logger.error('error with my database ',ex)
            answer = jsonify(message_500)
            answer.status_code = 500


    url = pdns_url + request.path
    app.logger.debug('start process %s query for %s, url is %s ', request.method, zone, url)
    if request.method == 'GET':
        try:
            app.logger.info('make %s request to pdns for zone %s',request.method, zone)
            res = requests.get(url, headers=headers)
            # Make right answer
            answer = jsonify(res.text)
            answer.status_code = res.status_code
            #answer.headers = res.headers
            app.logger.debug('response code from pdns %s',res.status_code)
        except Exception as ex:
            app.logger.error('something wrong %s',ex)
            answer = jsonify(message_500) 
            answer.status_code = 500

    else:
        deny = False
        app.logger.debug('analyze rrsets from request')
        try: 
            data = json.loads(request.data)
            for rrset in data['rrsets']:
                app.logger.debug('checking request %s for %s %s ',rrset['changetype'], rrset['type'], rrset['name'])
                # checking deny rules
                for row in Access.query.filter_by(login=login, zone=zone, mode='deny').all():
                    if (  (rrset['type'] == row.type or row.type == '*' ) and
                          (rrset['name'] == row.record or row.record == '*' ) 
                       ):
                        deny = True
                        app.logger.info('I found deny rule for %s %s %s Rule: %s %s %s %s', login, rrset['type'], rrset['name'], row.login, row.type, row.record, row.mode)

                # checking allowing rules if exist deny !!
                if deny:
                    for row in Access.query.filter_by(login=login, zone=zone, mode='allow').all():
                        if (rrset['type'] == row.type and rrset['name'] == row.record):
                            deny = False
                            app.logger.info('I found allow rule for %s Rule: %s %s %s %s' , login , row.login, row.type, row.record, row.mode)

            print("Do not make a request: " + str(deny))
            if not deny:
                res = requests.patch(url, headers=headers, data=json.dumps(data))
                answer = jsonify(res.text)
                answer.status_code = res.status_code
                #answer.headers = res.headers
            else:
                answer = jsonify(message_403)
                answer.status_code = 403
        except Exception as ex:
            app.logger.error('something wrong %s',ex);
            answer = jsonify(message_500) 
            answer.status_code = 500

    return answer


if __name__ == '__main__':
    app.run(debug=True)
