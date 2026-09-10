class Appointment:
    def __init__(
            self,
            appointment_id=None,
            patient_id=None,
            doctor_id=None,
            appointment_date=None,
            appointment_time=None,
            reason=None,
            status="Scheduled",
            created_at=None):

        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.reason = reason
        self.status = status
        self.created_at = created_at

    def __repr__(self):
        return (
            f"Appointment("
            f"appointment_id={self.appointment_id}, "
            f"patient_id={self.patient_id}, "
            f"doctor_id={self.doctor_id}, "
            f"appointment_date='{self.appointment_date}', "
            f"appointment_time='{self.appointment_time}', "
            f"reason='{self.reason}', "
            f"status='{self.status}', "
            f"created_at='{self.created_at}')"
        )