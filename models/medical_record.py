class MedicalRecord:
    def __init__(
        self,
        record_id=None,
        patient_id=None,
        doctor_id=None,
        diagnosis="",
        treatment="",
        prescription="",
        record_date=""
    ):
        self.record_id = record_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.diagnosis = diagnosis
        self.treatment = treatment
        self.prescription = prescription
        self.record_date = record_date

    def __repr__(self):
        return (
            f"MedicalRecord(record_id={self.record_id}, "
            f"patient_id={self.patient_id}, "
            f"doctor_id={self.doctor_id}, "
            f"diagnosis='{self.diagnosis}', "
            f"treatment='{self.treatment}', "
            f"prescription='{self.prescription}', "
            f"record_date='{self.record_date}')"
        )


