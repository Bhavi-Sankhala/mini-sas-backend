from app.modules.appointments.repository import AppointmentRepository
from app.modules.patients.repository import PatientRepository
from app.common.responses import success

class PatientService:

    @staticmethod
    def get_patient_by_id(patient_id):
        patient = PatientRepository.get_patient_by_id(patient_id)

        if not patient:
            return success({"message": "Patient not found"})

        return success(patient)

    @staticmethod
    def get_patient_appointment_view(appointment_id):
        appointment = AppointmentRepository.get_for_patient_view(appointment_id)

        if not appointment:
            return {
                "success": False,
                "data": None,
                "error": "Appointment not found"
            }, 404

        return {
            "success": True,
            "data": appointment,
            "error": None
        }, 200

    @staticmethod
    def get_patient_view(appointment_id):
        appointment = AppointmentRepository.get_for_patient_view(appointment_id)

        if not appointment:
            return {
                "success": False,
                "data": None,
                "error": "Appointment not found"
            }, 404

        return {
            "success": True,
            "data": appointment,
            "error": None
        }, 200

    @staticmethod
    def update_patient_details(appointment_id, data):
        result = AppointmentRepository.update_patient_details(appointment_id, data)

        if result == "APPOINTMENT_NOT_FOUND":
            return {
                "success": False,
                "data": None,
                "error": "Appointment not found"
            }, 404

        if result == "NO_FIELDS":
            return {
                "success": False,
                "data": None,
                "error": "No valid fields provided for update"
            }, 400

        return {
            "success": True,
            "data": {"appointment_id": appointment_id},
            "error": None
        }, 200