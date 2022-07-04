from flask import Blueprint, request, jsonify
from web_util import assert_data_has_keys
from web_errors import WebError
from users.user import User
import patients.data_access as Patient
import visits.data_access as Visits
from sync.db_sychronization import DbSynchronizer
import os
from pathlib import Path

mobile_api = Blueprint('mobile_api', __name__, url_prefix='/srvPy/api')


@mobile_api.route('/instances', methods=['GET'])
def all_instances():
    return jsonify(
        [{'name': 'Demo Instance', 'url': 'https://demo-api.hikmahealth.org'},
         {'name': 'EMA', 'url': 'https://ema-api.hikmahealth.org'},
         {'name': 'Local (testing)', 'url': 'http://192.168.86.250:8080'}]
    )


@mobile_api.route('/async', methods=['GET'])
def fetch_all():
    patients = Patient.fetch_patient_data()
    visits = Visits.all_visits()
    events = Visits.all_events()
    stringContent = Visits.all_string_content()
    stringIDS = Visits.all_string_ids()
    return{ "ok":"true"}
        # {'patients': jsonify(patients)},
        # {'visits':  jsonify(visits)},
        # {'events':  jsonify(events)},
        # {'stringContent':  jsonify(stringContent)},
        # {'stringIDS':  jsonify(stringIDS)}}


@mobile_api.route('/login', methods=['POST'])
def login():
    params = assert_data_has_keys(request, {'email', 'password'})
    user = User.authenticate(params['email'], params['password'])
    return jsonify(user.to_dict())


@mobile_api.route('/sync', methods=['POST'])
def sync():
    qa = os.path.expanduser('~')
    #params =  request.files['db']
    #f =  open('C:/Users/BasselEl-Bizri/AppData/wtv.txt','r')
    # print(params)
    print(os.path.expanduser('~'))
    return {"sta": qa}
    # params = assert_data_has_keys(request, {'email', 'password'}, data_type='form')
    # User.authenticate(params['email'], params['password'])
    # if 'db' not in request.files:
    #     raise WebError('db must be provided', 400)

    # synchronizer = DbSynchronizer(request.files['db'])
    # if not synchronizer.prepare_sync():
    #     raise WebError("Synchronization failed", 500)

    # synchronizer.execute_server_side_sql()
    # return jsonify({'to_execute': synchronizer.get_client_sql()})
