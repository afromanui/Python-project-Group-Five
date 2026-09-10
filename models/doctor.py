class Doctor:
    def __init__(
            self,
            doctor_id=None,
            user_id=None,
            first_name="",
            last_name="",
            specialization="",
            phone="",
            email="",


    ):

        self.doctor_id = doctor_id
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.specialization = specialization
        self.phone = phone
        self.email = email

    def __repr__(self):
        return (
            f"Doctor(doctor_id={self.doctor_id}, "
            f"name='{self.first_name} {self.last_name}', "
            f"specialization='{self.specialization}')"

        
        )