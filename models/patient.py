class Patient:
    def __init__(
        self,
        patient_id=None,
        first_name="",
        last_name="",
        date_of_birth="",
        gender="",
        phone="",
        address="",
        emergency_contact=""
    ):
        self.patient_id = patient_id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.phone = phone
        self.address = address
        self.emergency_contact = emergency_contact

    def __repr__(self):
        return (
            f"Patient("
            f"patient_id={self.patient_id}, "
            f"name='{self.first_name} {self.last_name}', "
            f"date_of_birth='{self.date_of_birth}', "
            f"gender='{self.gender}', "
            f"phone='{self.phone}', "
            f"address='{self.address}', "
            f"emergency_contact='{self.emergency_contact}'"
            f")"
        )