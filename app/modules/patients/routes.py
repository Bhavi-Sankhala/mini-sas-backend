from flask import request
from flask_restx import Namespace, Resource, fields
from app.extensions.db import SessionLocal
from sqlalchemy import text
from app.modules.appointments.service import AppointmentService
 

patient_ns = Namespace("patients", description="Patient Management")

# Model for Swagger JSON input
patient_model = patient_ns.model('PatientModel', {
    'patient_id': fields.String(required=True, example='PAT-001'),
    'full_name': fields.String(required=True, example='Bhagirath Manda'),
    'phone_number': fields.String(example='1234567890'),
    'email': fields.String(example='test@example.com')
})

@patient_ns.route("")
class PatientList(Resource):
    @patient_ns.expect(patient_model)
    def post(self):
        """Add a new patient via JSON"""
        data = request.json
        session = SessionLocal()
        try:
            query = text("""
                INSERT INTO patients (patient_id, full_name, phone_number, email)
                VALUES (:patient_id, :full_name, :phone_number, :email)
                RETURNING id
            """)
            session.execute(query, data)
            session.commit()
            return {"success": True, "message": "Patient created"}, 201
        finally:
            session.close()


from flask_restx import Namespace, Resource
from app.modules.patients.service import PatientService


@patient_ns.route("/<string:patient_id>")
class GetPatient(Resource):
    def get(self, patient_id):
        """
        Get patient details by patient_id
        """
        return PatientService.get_patient_by_id(patient_id)

@patient_ns.route("/appointment/<string:appointment_id>/view")
class PatientAppointmentView(Resource):
    def get(self, appointment_id):
        result, status_code = AppointmentService.get_patient_view(appointment_id)
        return result, status_code

update_patient_model = patient_ns.model(
    "UpdatePatientDetails",
    {
        "phone_number": fields.String(example="8888888888"),
        "email": fields.String(example="updated@example.com"),
        "fullName": fields.String(example="Patient Updated")
    }
)

@patient_ns.route("/appointment/<string:appointment_id>/update")
class PatientUpdateDetails(Resource):

    @patient_ns.expect(update_patient_model)
    def patch(self, appointment_id):
        data = request.get_json() or {}
        return AppointmentService.update_patient_details(appointment_id, data)
