from flask import Blueprint, request, jsonify
from web_util import assert_data_has_keys
#from patients.patient import Patient
import patients.data_access as Patient
patient_api = Blueprint('patients_api', __name__, url_prefix='/api/patient')


@patient_api.route('/get_patients', methods=['GET'])
def sync():
    patients = Patient.get_all_patient()
    print(patients)
    return jsonify({'results': patients})
