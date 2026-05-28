from app.modules.notifications.repository import NotificationRepository


class NotificationService:

    @staticmethod
    def get_patient_notifications(patient_id):
        notifications = NotificationRepository.get_by_patient(patient_id)

        return {
            "success": True,
            "data": notifications,
            "error": None
        }, 200

    @staticmethod
    def mark_notification_read(notification_id):
        NotificationRepository.mark_as_read(notification_id)

        return {
            "success": True,
            "data": {"notification_id": notification_id},
            "error": None
        }, 200
