from flask import Blueprint, request, jsonify
from web_util import assert_data_has_keys
from clinics.clinic import Clinic

clinic_api = Blueprint('clinics_api', __name__, url_prefix='/api/clinics')


@clinic_api.route('/get_clinics', methods=['GET'])
def sync():
    clinic =  Clinic.get_all_clinic()
    print(clinic)
    return jsonify({'results': clinic})
