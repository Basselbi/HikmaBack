from flask import Blueprint, request, jsonify
from web_util import assert_data_has_keys
from web_errors import WebError
from users.user import User
import patients.data_access as Patient
import visits.data_access as Visits
import sync.data_access as Synx
from sync.db_sychronization import DbSynchronizer
import os
from pathlib import Path
import sqlite3
from werkzeug.datastructures import FileStorage

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

@mobile_api.route('/as', methods=['POST'])
def update_edited_at(table_name):
    server_ids = Synx.get_string_ids_and_edit_timestamps_only(table_name)
    for id, ts in server_ids:
        if "+00" in ts:
            withoutZero = ts.replace("+00", "Z")
            withoutSpace = withoutZero.replace(" ", "T")
            Synx.update_ts(id,withoutSpace,table_name)

    #withoutZero =  server_ids[id].replace("+00", "Z")
    #withoutSpace = withoutZero.replace("+00", "Z")
    return jsonify({'to_execute': "synchronizer.get_client_sql()"})
@mobile_api.route('/sync', methods=['POST'])
def sync():
    update_edited_at("clinics")
    update_edited_at("events")
    update_edited_at("patients")
    update_edited_at("string_content")
    update_edited_at("visits")
    qa = os.path.expanduser('~')
    #params =  request.files['db']
    #f =  open('C:/Users/BasselEl-Bizri/AppData/wtv.txt','r')
    # print(params)
    print(os.path.expanduser('~'))
    params = assert_data_has_keys(request, {'sql'})
    sql = params['sql']
    sqlArr = sql.split(';')
    #print(sqlArr)
    # params = assert_data_has_keys(request, {'email', 'password'}, data_type='form')
    # User.authenticate(params['email'], params['password'])
    # if 'db' not in request.files:
    #     raise WebError('db must be provided', 400)
    if os.path.exists("/tmp/sql3_hk_tmp.db"):
       os.remove("/tmp/sql3_hk_tmp.db")
       print('Hk Tmp Removed')
    connection = sqlite3.connect("/tmp/sql3_hk_tmp.db")
    cursor = connection.cursor()
    for qrySql in sqlArr:
        print(qrySql)
        cursor.execute(qrySql)
    # connection 
    connection.commit() 
    connection.close()        
    #rows = cursor.execute("SELECT * from patients ").fetchall()
    #print(len(sqlArr))
    #print(rows)
    file = None
    with open('/tmp/sql3_hk_tmp.db', 'rb') as fp:
        file = FileStorage(fp)
        synchronizer = DbSynchronizer(file)
     
    if not synchronizer.prepare_sync():
        raise WebError("Synchronization failed", 500)

    synchronizer.execute_server_side_sql()
    os.remove("/tmp/sql3_hk_tmp.db")
    return jsonify({'to_execute': synchronizer.get_client_sql()})
