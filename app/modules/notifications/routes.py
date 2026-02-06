from flask_restx import Namespace, Resource
from app.modules.notifications.service import NotificationService

notification_ns = Namespace(
    "notifications",
    description="Patient Notification APIs"
)


@notification_ns.route("/patient/<string:patient_id>")
class PatientNotifications(Resource):
    def get(self, patient_id):
        """
        Get all notifications for a patient
        """
        return NotificationService.get_patient_notifications(patient_id)


# UUID → string
@notification_ns.route("/<string:notification_id>/read")
class MarkNotificationRead(Resource):
    def patch(self, notification_id):
        """
        Mark a notification as read
        """
        return NotificationService.mark_notification_read(notification_id)
