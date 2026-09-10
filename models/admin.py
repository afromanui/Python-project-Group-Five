class Admin:
    def __init__(
        self,
        admin_id=None,
        user_id=None,
        username="",
        password_hash="",
        full_name="",
        email="",
        phone=""
    ):
        self.admin_id = admin_id
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.full_name = full_name
        self.email = email
        self.phone = phone

    def __repr__(self):
        return (
            f"Admin(admin_id={self.admin_id}, "
            f"user_id={self.user_id}, "
            f"username='{self.username}', "
            f"full_name='{self.full_name}', "
            f"email='{self.email}')"
        )