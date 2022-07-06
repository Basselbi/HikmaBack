from db_util import get_connection
import datetime
from visits.visit import Visit
from typing import Tuple, Optional


def add_visit(visit: Visit):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO visits (id, patient_id, clinic_id, provider_id, check_in_timestamp, edited_at) VALUES (%s, %s, %s, %s, %s, %s)',
                        [visit.id,
                         visit.patient_id,
                         visit.clinic_id,
                         visit.provider_id,
                         visit.check_in_timestamp,
                         visit.edited_at
                         ])
def all_visits_sync():
    qry = """ SELECT * FROM visits WHERE deleted = %s ORDER BY check_in_timestamp DESC;"""
    arr = []
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(qry, [0])
            for row in cur:
                arr.append("insert into visits values " + str(row) + ";");
            return arr

def all_string_content():
    qry = """ SELECT * FROM string_content"""
    arr = []
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(qry, [])
            for row in cur:
                arr.append("insert into string_content values " + str(row) + ";");
            return arr     
        
def all_string_ids():
    qry = """ SELECT * FROM string_ids"""
    arr = []
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(qry, [])
            for row in cur:
                arr.append("insert into string_ids values " + str(row) + ";");
            return arr

def all_events():
    qry = """ SELECT * FROM events"""
    arr = []
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(qry, [])
            for row in cur:
                arr.append("insert into events values " + str(row) + ";");
            return arr             
def first_visit_by_patient_and_date(patient_id: str, date: datetime.date) -> Tuple[Optional[str], Optional[str]]:
    query = "SELECT id, check_in_timestamp FROM visits WHERE patient_id = %s AND date(check_in_timestamp) = %s;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, [patient_id, date])
            row = cur.fetchone()
            if row is None:
                return None, None
            else:
                return row[0], row[1]


def all_visits():
    query = "SELECT id, patient_id, clinic_id, provider_id, check_in_timestamp, edited_at, deleted FROM visits WHERE not deleted ORDER BY check_in_timestamp DESC;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, [])
            for row in cur:
                yield Visit(
                    id=row[0],
                    patient_id=row[1],
                    clinic_id=row[2],
                    provider_id=row[3],
                    check_in_timestamp=row[4],
                    edited_at=row[5],
                    deleted=row[6]
                )


def patient_visits(patient_id: str):
    query = "SELECT id, patient_id, clinic_id, provider_id, check_in_timestamp, edited_at, deleted FROM visits WHERE patient_id = %s AND not deleted ORDER BY check_in_timestamp DESC;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, [patient_id])
            for row in cur:
                yield Visit(
                    id=row[0],
                    patient_id=row[1],
                    clinic_id=row[2],
                    provider_id=row[3],
                    check_in_timestamp=row[4],
                    edited_at=row[5],
                    deleted=row[6]
                )