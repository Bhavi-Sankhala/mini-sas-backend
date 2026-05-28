from sqlalchemy import text
from app.extensions.db import SessionLocal

class NotificationRepository:

    @staticmethod
    def get_by_patient(patient_id):
        session = SessionLocal()
        try:
            query = text("""
                SELECT
                    id,
                    patient_id,
                    title,
                    message,
                    is_read,
                    created_at
                FROM notifications
                WHERE patient_id = :patient_id
                ORDER BY created_at DESC
            """)

            result = session.execute(
                query,
                {"patient_id": patient_id}
            ).mappings().all()   # ✅ IMPORTANT

            return [
                {
                    "id": str(row["id"]),
                    "patient_id": row["patient_id"],
                    "title": row["title"],
                    "message": row["message"],
                    "is_read": row["is_read"],
                    "created_at": row["created_at"].isoformat()
                }
                for row in result
            ]

        finally:
            session.close()

    @staticmethod
    def mark_as_read(notification_id):
        session = SessionLocal()
        try:
            query = text("""
                UPDATE notifications
                SET is_read = TRUE
                WHERE id = :notification_id
            """)

            session.execute(query, {"notification_id": notification_id})
            session.commit()

        finally:
            session.close()