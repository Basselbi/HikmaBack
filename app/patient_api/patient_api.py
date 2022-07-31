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
    patients = Patient.fetch_patient_data()
    print(patients)
    return jsonify({'results': patients})

 
@patient_api.route('/add_patient', methods=['POST'])
def add_patient():
    params = assert_data_has_keys(request, {'id', 'name'})
    pat    = params['id']
    print(pat)
    # patient = Patient(
    #     id=str(uuid.uuid4()),
    #     edited_at=datetime.now(),
    #     given_name=given_name_ls,
    #     surname=surname_ls,
    #     date_of_birth=date(2000, 10, 31),
    #     sex=sex,
    #     country=LanguageString(id=str(uuid.uuid4()), content_by_language={'en': 'Syria'}),
    #     hometown=LanguageString(id=str(uuid.uuid4()), content_by_language={'en': 'Damascus'}),
    #     phone=None
    # )    
    #patients = Patient.add_patient()
    #print(patients)
    return jsonify(params)
