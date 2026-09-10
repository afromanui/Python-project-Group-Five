import hashlib

from database.database_manager import DatabaseManager


class AuthService:
    """
    Handles user registration and authentication using MySQL.
    """

    def __init__(self):
        self.database = DatabaseManager()

    # =========================================================
    # PASSWORD HASHING
    # =========================================================

    @staticmethod
    def hash_password(password):
        """
        Convert a password into a SHA-256 hash.
        """

        if password is None:
            return ""

        return hashlib.sha256(
            password.encode("utf-8")
        ).hexdigest()

    # =========================================================
    # SIGN UP / REGISTER USER
    # =========================================================

    def register_user(
        self,
        username,
        password,
        confirm_password=None,
        role="Staff"
    ):
        """
        Register a new user.

        Parameters:
            username: Username for the new account.
            password: Password for the new account.
            confirm_password: Password confirmation.
            role: User role.

        Returns:
            (True, message) when successful.
            (False, message) when registration fails.
        """

        # -----------------------------------------------------
        # Validate username
        # -----------------------------------------------------

        if username is None:
            return False, "Username is required."

        username = username.strip()

        if not username:
            return False, "Username is required."

        if len(username) < 3:
            return False, "Username must be at least 3 characters."

        # -----------------------------------------------------
        # Validate password
        # -----------------------------------------------------

        if password is None:
            return False, "Password is required."

        # Do NOT strip passwords.
        # Spaces may technically be part of a password.

        if password == "":
            return False, "Password is required."

        if len(password) < 4:
            return False, "Password must be at least 4 characters."

        # -----------------------------------------------------
        # Validate confirmation password
        # -----------------------------------------------------

        if confirm_password is None:
            return False, "Please confirm your password."

        if confirm_password == "":
            return False, "Please confirm your password."

        if password != confirm_password:
            return False, "Passwords do not match."

        # -----------------------------------------------------
        # Validate role
        # -----------------------------------------------------

        if role is None:
            role = "Staff"

        role = str(role).strip()

        if not role:
            role = "Staff"

        allowed_roles = (
            "Staff",
            "Doctor",
            "Administrator"
        )

        if role not in allowed_roles:
            role = "Staff"

        # -----------------------------------------------------
        # Connect to MySQL
        # -----------------------------------------------------

        connection = self.database.get_connection()

        if connection is None:
            return (
                False,
                "Unable to connect to the MySQL database."
            )

        cursor = None

        try:

            cursor = connection.cursor(
                dictionary=True
            )

            # -------------------------------------------------
            # Check whether username already exists
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT
                    user_id
                FROM users
                WHERE username = %s
                LIMIT 1
                """,
                (username,)
            )

            existing_user = cursor.fetchone()

            if existing_user:

                return (
                    False,
                    "That username already exists."
                )

            # -------------------------------------------------
            # Hash password
            # -------------------------------------------------

            password_hash = self.hash_password(
                password
            )

            # -------------------------------------------------
            # Insert new user
            # -------------------------------------------------

            cursor.execute(
                """
                INSERT INTO users
                (
                    username,
                    password_hash,
                    role
                )
                VALUES
                (
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    username,
                    password_hash,
                    role
                )
            )

            connection.commit()

            return (
                True,
                "Account created successfully."
            )

        except Exception as error:

            try:
                connection.rollback()
            except Exception:
                pass

            return (
                False,
                f"Registration error: {error}"
            )

        finally:

            if cursor is not None:

                try:
                    cursor.close()
                except Exception:
                    pass

            try:
                connection.close()
            except Exception:
                pass

    # =========================================================
    # SIGN IN / LOGIN
    # =========================================================

    def login(self, username, password):
        """
        Authenticate a user.

        Returns:
            User dictionary when successful.
            None when authentication fails.
        """

        if username is None:
            return None

        if password is None:
            return None

        username = username.strip()

        if not username:
            return None

        if password == "":
            return None

        connection = self.database.get_connection()

        if connection is None:
            return None

        cursor = None

        try:

            cursor = connection.cursor(
                dictionary=True
            )

            # -------------------------------------------------
            # Find user
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT
                    user_id,
                    username,
                    password_hash,
                    role
                FROM users
                WHERE username = %s
                LIMIT 1
                """,
                (username,)
            )

            user = cursor.fetchone()

            # -------------------------------------------------
            # User does not exist
            # -------------------------------------------------

            if user is None:
                return None

            # -------------------------------------------------
            # Hash entered password
            # -------------------------------------------------

            entered_password_hash = self.hash_password(
                password
            )

            # -------------------------------------------------
            # Compare password hashes
            # -------------------------------------------------

            stored_password_hash = user.get(
                "password_hash"
            )

            if stored_password_hash != entered_password_hash:
                return None

            # -------------------------------------------------
            # Successful login
            # -------------------------------------------------

            return {
                "user_id": user.get("user_id"),
                "username": user.get("username"),
                "role": user.get("role", "Staff")
            }

        except Exception as error:

            print(
                f"Login error: {error}"
            )

            return None

        finally:

            if cursor is not None:

                try:
                    cursor.close()
                except Exception:
                    pass

            try:
                connection.close()
            except Exception:
                pass

    # =========================================================
    # GET ALL USERS
    # =========================================================

    def get_all_users(self):
        """
        Return all registered users.

        Password hashes are intentionally NOT returned.
        """

        connection = self.database.get_connection()

        if connection is None:
            return []

        cursor = None

        try:

            cursor = connection.cursor(
                dictionary=True
            )

            cursor.execute(
                """
                SELECT
                    user_id,
                    username,
                    role
                FROM users
                ORDER BY user_id ASC
                """
            )

            return cursor.fetchall()

        except Exception as error:

            print(
                f"Error getting users: {error}"
            )

            return []

        finally:

            if cursor is not None:

                try:
                    cursor.close()
                except Exception:
                    pass

            try:
                connection.close()
            except Exception:
                pass

    # =========================================================
    # FIND USER
    # =========================================================

    def get_user(self, username):
        """
        Find a user by username.

        Password hashes are intentionally NOT returned.
        """

        if username is None:
            return None

        username = username.strip()

        if not username:
            return None

        connection = self.database.get_connection()

        if connection is None:
            return None

        cursor = None

        try:

            cursor = connection.cursor(
                dictionary=True
            )

            cursor.execute(
                """
                SELECT
                    user_id,
                    username,
                    role
                FROM users
                WHERE username = %s
                LIMIT 1
                """,
                (username,)
            )

            return cursor.fetchone()

        except Exception as error:

            print(
                f"Error finding user: {error}"
            )

            return None

        finally:

            if cursor is not None:

                try:
                    cursor.close()
                except Exception:
                    pass

            try:
                connection.close()
            except Exception:
                pass


# =============================================================
# TEST AUTHENTICATION SERVICE
# =============================================================

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("AUTHENTICATION SERVICE - MYSQL TEST")
    print("=" * 60)

    try:

        auth = AuthService()

        connection = auth.database.get_connection()

        if connection:

            print("MySQL connection: SUCCESS")
            print("Database: hospital_management")

            connection.close()

            users = auth.get_all_users()

            print(
                f"Registered users: {len(users)}"
            )

            if users:

                print()
                print("Registered accounts:")

                for user in users:

                    print(
                        f"  ID: {user.get('user_id')} | "
                        f"Username: {user.get('username')} | "
                        f"Role: {user.get('role')}"
                    )

            else:

                print()
                print("No users are registered yet.")

        else:

            print("MySQL connection: FAILED")
            print()
            print(
                "Please make sure MySQL is running "
                "in XAMPP and the database "
                "'hospital_management' exists."
            )

    except Exception as error:

        print(
            f"Authentication service test error: {error}"
        )

    print("=" * 60)
    print()