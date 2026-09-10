import mysql.connector
from mysql.connector import Error


class AdministratorService:
    """
    Administrator Service
    Handles all administrator operations using MySQL/MariaDB.
    """

    DB_CONFIG = {
        "host": "127.0.0.1",
        "user": "root",
        "password": "",
        "database": "hospital_management",
        "port": 3306
    }

    # ============================================================
    # DATABASE CONNECTION
    # ============================================================

    def _get_connection(self):
        """Create a connection to the hospital_management database."""

        try:
            connection = mysql.connector.connect(
                host=self.DB_CONFIG["host"],
                user=self.DB_CONFIG["user"],
                password=self.DB_CONFIG["password"],
                database=self.DB_CONFIG["database"],
                port=self.DB_CONFIG["port"]
            )

            return connection

        except Error as error:
            print(f"MySQL connection error: {error}")
            return None

    # ============================================================
    # ADD ADMINISTRATOR
    # ============================================================

    def add_administrator(
        self,
        full_name,
        email="",
        phone=""
    ):
        """Add a new administrator."""

        connection = None
        cursor = None

        try:
            full_name = str(full_name).strip()
            email = str(email).strip()
            phone = str(phone).strip()

            if not full_name:
                print("Administrator name is required.")
                return None

            connection = self._get_connection()

            if connection is None:
                return None

            cursor = connection.cursor()

            query = """
                INSERT INTO administrators
                (
                    full_name,
                    email,
                    phone
                )
                VALUES
                (
                    %s,
                    %s,
                    %s
                )
            """

            values = (
                full_name,
                email,
                phone
            )

            cursor.execute(query, values)

            admin_id = cursor.lastrowid

            connection.commit()

            print(
                f"Administrator added successfully. "
                f"Admin ID: {admin_id}"
            )

            return {
                "admin_id": admin_id,
                "full_name": full_name,
                "email": email,
                "phone": phone
            }

        except Error as error:

            if connection:
                connection.rollback()

            print(
                f"MySQL error while adding administrator: {error}"
            )

            return None

        finally:

            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()

    # ============================================================
    # GET ALL ADMINISTRATORS
    # ============================================================

    def get_all_administrators(self):
        """
        Return all administrators as dictionaries.
        """

        connection = None
        cursor = None

        try:
            connection = self._get_connection()

            if connection is None:
                return []

            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT
                    admin_id,
                    user_id,
                    full_name,
                    email,
                    phone
                FROM administrators
                ORDER BY admin_id DESC
            """

            cursor.execute(query)

            return cursor.fetchall()

        except Error as error:

            print(
                f"MySQL error while loading administrators: {error}"
            )

            return []

        finally:

            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()

    # ============================================================
    # GET ONE ADMINISTRATOR
    # ============================================================

    def get_administrator(self, admin_id):
        """Return one administrator by ID as a dictionary."""

        connection = None
        cursor = None

        try:
            connection = self._get_connection()

            if connection is None:
                return None

            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT
                    admin_id,
                    user_id,
                    full_name,
                    email,
                    phone
                FROM administrators
                WHERE admin_id = %s
            """

            cursor.execute(
                query,
                (admin_id,)
            )

            return cursor.fetchone()

        except Error as error:

            print(
                f"MySQL error while loading administrator: {error}"
            )

            return None

        finally:

            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()

    # ============================================================
    # UPDATE ADMINISTRATOR
    # ============================================================

    def update_administrator(
        self,
        admin_id,
        full_name,
        email="",
        phone=""
    ):
        """Update an existing administrator."""

        connection = None
        cursor = None

        try:
            full_name = str(full_name).strip()
            email = str(email).strip()
            phone = str(phone).strip()

            if not full_name:
                print("Administrator name is required.")
                return False

            connection = self._get_connection()

            if connection is None:
                return False

            cursor = connection.cursor()

            # Check that administrator exists
            cursor.execute(
                """
                SELECT admin_id
                FROM administrators
                WHERE admin_id = %s
                """,
                (admin_id,)
            )

            if cursor.fetchone() is None:
                print(
                    f"Administrator {admin_id} not found."
                )
                return False

            query = """
                UPDATE administrators
                SET
                    full_name = %s,
                    email = %s,
                    phone = %s
                WHERE admin_id = %s
            """

            values = (
                full_name,
                email,
                phone,
                admin_id
            )

            cursor.execute(query, values)

            connection.commit()

            print(
                f"Administrator {admin_id} "
                f"updated successfully."
            )

            return True

        except Error as error:

            if connection:
                connection.rollback()

            print(
                f"MySQL error while updating administrator: {error}"
            )

            return False

        finally:

            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()

    # ============================================================
    # DELETE ADMINISTRATOR
    # ============================================================

    def delete_administrator(self, admin_id):
        """Delete an administrator by ID."""

        connection = None
        cursor = None

        try:
            connection = self._get_connection()

            if connection is None:
                return False

            cursor = connection.cursor()

            # Check administrator exists
            cursor.execute(
                """
                SELECT admin_id
                FROM administrators
                WHERE admin_id = %s
                """,
                (admin_id,)
            )

            if cursor.fetchone() is None:
                print(
                    f"Administrator {admin_id} not found."
                )
                return False

            # Delete administrator
            query = """
                DELETE FROM administrators
                WHERE admin_id = %s
            """

            cursor.execute(
                query,
                (admin_id,)
            )

            connection.commit()

            print(
                f"Administrator {admin_id} "
                f"deleted successfully."
            )

            return True

        except Error as error:

            if connection:
                connection.rollback()

            print(
                f"MySQL error while deleting administrator: {error}"
            )

            return False

        finally:

            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()

    # ============================================================
    # TEST DATABASE CONNECTION
    # ============================================================

    def test_connection(self):
        """Test the MySQL database connection."""

        connection = None

        try:
            connection = self._get_connection()

            if connection and connection.is_connected():
                return True

            return False

        except Error as error:

            print(
                f"MySQL connection test error: {error}"
            )

            return False

        finally:

            if connection and connection.is_connected():
                connection.close()


# ================================================================
# TEST ADMINISTRATOR SERVICE
# ================================================================

if __name__ == "__main__":

    service = AdministratorService()

    print("=" * 60)
    print("ADMINISTRATOR SERVICE - MYSQL TEST")
    print("=" * 60)

    if service.test_connection():

        print("MySQL connection: SUCCESS")

        administrators = service.get_all_administrators()

        print(
            f"Administrators found: {len(administrators)}"
        )

        for administrator in administrators:
            print(administrator)

    else:

        print("MySQL connection: FAILED")

    print("=" * 60)