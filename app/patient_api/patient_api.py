from flask import Blueprint, request, jsonify
from web_util import assert_data_has_keys
#from patients.patient import Patient
import patients.data_access as Patient
patient_api = Blueprint('patients_api', __name__, url_prefix='/srvPy/api/patient')


@patient_api.route('/get_patients', methods=['GET'])
def sync():
    patients = Patient.get_all_patient()
    print(patients)
    return jsonify({'results': patients})

@patient_api.route('/get_recent_patients', methods=['GET'])
def recent_patient():
    patients = Patient.get_recent_patients('2022-07-03T02:12:17.709Z')
    #print(patients)
    return jsonify({'results': patients})

 
