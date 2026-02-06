from sqlalchemy import text
from app.extensions.db import SessionLocal

class PatientRepository:

    @staticmethod
    def get_patient_by_id(patient_id):
        session = SessionLocal()
        try:
            query = text("""
                SELECT
                    patient_id,
                    full_name,
                    phone_number,
                    email,
                    is_verified,
                    created_at
                FROM patients
                WHERE patient_id = :patient_id
            """)

            result = session.execute(
                query,
                {"patient_id": patient_id}
            ).fetchone()

            if not result:
                return None

            return {
                "patient_id": result.patient_id,
                "full_name": result.full_name,
                "phone_number": result.phone_number,
                "email": result.email,
                "is_verified": result.is_verified,
                "created_at": result.created_at.isoformat() if result.created_at else None
            }

        finally:
            session.close()

    @staticmethod
    def get_for_patient_view(appointment_id):
        session = SessionLocal()
        try:
            query = text("""
                SELECT
                    a.appointment_id,
                    a.slot_time::TEXT AS slot_time,
                    a.status,
                    a.provider_id,
                    p.patient_id,
                    p.full_name,
                    p.phone_number,
                    p.email
                FROM appointments a
                JOIN patients p ON a.patient_id = p.patient_id
                WHERE a.appointment_id = :appointment_id
            """)

            result = session.execute(
                query,
                {"appointment_id": appointment_id}
            ).mappings().fetchone()

            if not result:
                return None

            return dict(result)

        finally:
            session.close()

    @staticmethod
    def update_patient_details(appointment_id, data):
        session = SessionLocal()
        try:
            appt = session.execute(
                text("""
                    SELECT patient_id
                    FROM appointments
                    WHERE appointment_id = :appointment_id
                """),
                {"appointment_id": appointment_id}
            ).fetchone()

            if not appt:
                return "APPOINTMENT_NOT_FOUND"

            patient_id = appt.patient_id

            fields = []
            params = {"patient_id": patient_id}

            if "phone_number" in data:
                fields.append("phone_number = :phone_number")
                params["phone_number"] = data["phone_number"]

            if "email" in data:
                fields.append("email = :email")
                params["email"] = data["email"]

            if "fullName" in data:
                fields.append("full_name = :full_name")
                params["full_name"] = data["fullName"]

            if not fields:
                return "NO_FIELDS"

            update_query = text(f"""
                UPDATE patients
                SET {", ".join(fields)}
                WHERE patient_id = :patient_id
            """)

            session.execute(update_query, params)
            session.commit()

            return "UPDATED"

        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def get_billing_by_patient(patient_id):
        session = SessionLocal()
        try:
            query = text("""
                SELECT
                    invoice_id,
                    amount,
                    status,
                    paid_date
                FROM billing
                WHERE patient_id = :patient_id
                ORDER BY created_at DESC
            """)

            result = session.execute(
                query,
                {"patient_id": patient_id}
            ).mappings().all()

            return [
                {
                    "invoice_id": row["invoice_id"],
                    "amount": float(row["amount"]),
                    "status": row["status"],
                    "paid_date": (
                        row["paid_date"].isoformat()
                        if row["paid_date"] else None
                    )
                }
                for row in result
            ]

        finally:
            session.close()