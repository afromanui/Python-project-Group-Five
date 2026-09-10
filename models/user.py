class User:
    def __init__(self, user_id=None, username="", password_hash="", role=""):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.role = role

    def __repr__(self):
        return f"User(user_id={self.user_id}, username='{self.username}', role='{self.role}')"
