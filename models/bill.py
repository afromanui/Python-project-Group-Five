class Bill:
    def __init__(
        self,
        bill_id=None,
        patient_id=None,
        appointment_id=None,
        amount=0.0,
        payment_status="",
        bill_date=""
    ):
        self.bill_id = bill_id
        self.patient_id = patient_id
        self.appointment_id = appointment_id
        self.amount = amount
        self.payment_status = payment_status
        self.bill_date = bill_date

    def __repr__(self):
        return (
            f"Bill("
            f"bill_id={self.bill_id}, "
            f"patient_id={self.patient_id}, "
            f"appointment_id={self.appointment_id}, "
            f"amount={self.amount}, "
            f"payment_status='{self.payment_status}', "
            f"bill_date='{self.bill_date}'"
            f")"
        )