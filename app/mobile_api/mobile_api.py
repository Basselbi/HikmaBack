from flask import Blueprint, request, jsonify
from web_util import assert_data_has_keys
from web_errors import WebError
from users.user import User
import patients.data_access as Patient
import visits.data_access as Visits
from sync.db_sychronization import DbSynchronizer
import os
from pathlib import Path
import sqlite3
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
    results = []
    patients = Patient.fetch_patient_data()
    for row in patients:
        results.append(row)
    visits = Visits.all_visits_sync()
    for row in visits:
        results.append(row)
    events = Visits.all_events()
    for row in events:
        results.append(row)
    stringContent = Visits.all_string_content()
    for row in stringContent:
        results.append(row)
    stringIDS = Visits.all_string_ids()
    for row in stringIDS:
        results.append(row)    
    #results = patients + visits + events + stringContent + stringIDS 
    return{"results": results}

  

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
    params = assert_data_has_keys(request, {'sql'})
    sql = params['sql']
    sqlArr = sql.split(';')
    print(sqlArr)
    # params = assert_data_has_keys(request, {'email', 'password'}, data_type='form')
    # User.authenticate(params['email'], params['password'])
    # if 'db' not in request.files:
    #     raise WebError('db must be provided', 400)
    if os.path.exists("sql3_hk_tmp.db"):
       os.remove("sql3_hk_tmp.db")
    connection = sqlite3.connect("sql3_hk_tmp.db")
    cursor = connection.cursor()
    rows = cursor.execute("SELECT name, species, tank_number FROM fish").fetchall()
    print(len(sqlArr))
    #synchronizer = DbSynchronizer(request.files['db'])
    return {"sta": qa}
    # if not synchronizer.prepare_sync():
    #     raise WebError("Synchronization failed", 500)

    # synchronizer.execute_server_side_sql()
    # return jsonify({'to_execute': synchronizer.get_client_sql()})
