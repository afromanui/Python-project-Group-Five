class Receptionist:
    def __init__(
            self, 
            receptionist_id=None,
            user_id=None,
            first_name="",
            last_name="",
            phone="",
            email="",

    ):

            self.receptionist_id = receptionist_id
            self.user_id = user_id
            self.first_name = first_name
            self.last_name = last_name
            self.phone = phone
            self.email = email

    def __repr__(self):
        return (
              f"Receptionist(receptionist_id={self.receptionist_id}, "
              f"name='{self.first_name} {self.last_name}')"

        )
    
