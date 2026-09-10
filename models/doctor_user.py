from .user import User


class DoctorUser(User):
    def __init__(self, user_id=None, username="", password_hash=""):
        super().__init__(
            user_id=user_id,
            username=username,
            password_hash=password_hash,
            role="Doctor"
        )

    def __repr__(self):
        return f"DoctorUser(user_id={self.user_id}, username='{self.username}')"


if __name__ == "__main__":
    doctor = DoctorUser(
        user_id=1,
        username="doctor1",
        password_hash="test123"
    )

    print(doctor)