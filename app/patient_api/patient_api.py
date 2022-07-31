from flask import Blueprint, request, jsonify
from web_util import assert_data_has_keys
#from patients.patient import Patient
import patients.data_access as Patient
from datetime import datetime, date
from patients.patient import Patient as pt
import sqlite3

patient_api = Blueprint('patients_api', __name__, url_prefix='/srvPy/api/patient')


@patient_api.route('/get_patients', methods=['GET'])
def sync():
    patients = Patient.get_all_patient()
    print(patients)
    return jsonify({'results': patients})

@patient_api.route('/get_recent_patients', methods=['GET'])
def recent_patient():
    patients = Patient.fetch_patient_data()
    print(patients)
    return jsonify({'results': patients})

 
@patient_api.route('/add_patient', methods=['POST'])
def add_patient():
    params = assert_data_has_keys(request, {'id', 'given_name', 'surname', 'date_of_birth', 'sex', 'country', 'hometown', 'phone'})
    id    = params['id']
    given_name_ls    = params['given_name']
    surname_ls   = params['surname']
    date_of_birth = params['date_of_birth']
    sex = params['sex']
    country = params['country']
    hometown = params['hometown']
    phone = params['phone']
   #date(2000, 10, 31).isoformat(),
    patient = pt(
        id=str(id),
        edited_at=datetime.now().isoformat(),
        given_name=given_name_ls,
        surname=surname_ls,
        date_of_birth='03-54-21',
        sex=sex,
        country=country,
        hometown=hometown,
        phone=phone 
    )    
    print(patient)
    connection = sqlite3.connect("aquarium.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE fish (name TEXT, species TEXT, tank_number INTEGER)")
    cursor.execute("INSERT INTO fish VALUES ('Sammy', 'shark', 1)")
    cursor.execute("INSERT INTO fish VALUES ('Jamie', 'cuttlefish', 7)")
    #rows = cursor.execute("SELECT name, species, tank_number FROM fish").fetchall()
    #print(rows)
    #print(patients)
    return jsonify({})
