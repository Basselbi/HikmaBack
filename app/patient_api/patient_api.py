from flask import Blueprint, request, jsonify
from web_util import assert_data_has_keys
#from patients.patient import Patient
import patients.data_access as Patient
from datetime import datetime, date
from patients.patient import Patient as pt

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
   
    patient = pt(
        id=str(id),
        edited_at=datetime.now().isoformat(),
        given_name=given_name_ls,
        surname=surname_ls,
        date_of_birth=date(2000, 10, 31).isoformat(),
        sex=sex,
        country=country,
        hometown=hometown,
        phone=phone 
    )    
    print(patient)
    Patient.add_patient(patient)
    #print(patients)
    return jsonify(patient)
