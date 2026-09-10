from mysql.connector import Error

from database.database_manager import DatabaseManager
from models.doctor import Doctor


class DoctorService:
    """Handles doctor database operations using MySQL."""

    def __init__(self):
        self.database_manager = DatabaseManager()

    # =========================================================
    # ADD DOCTOR
    # =========================================================

    def add_doctor(
        self,
        first_name,
        last_name,
        specialization="",
        phone="",
        email=""
    ):
        """Add a new doctor."""

        connection = self.database_manager.get_connection()

        if connection is None:
            return None

        cursor = connection.cursor()

        try:
            sql = """
                INSERT INTO doctors
                (
                    first_name,
                    last_name,
                    specialization,
                    phone,
                    email
                )
                VALUES (%s, %s, %s, %s, %s)
            """

            values = (
                first_name.strip(),
                last_name.strip(),
                specialization.strip(),
                phone.strip(),
                email.strip()
            )

            cursor.execute(sql, values)
            connection.commit()

            doctor_id = cursor.lastrowid

            return Doctor(
                doctor_id=doctor_id,
                first_name=first_name.strip(),
                last_name=last_name.strip(),
                specialization=specialization.strip(),
                phone=phone.strip(),
                email=email.strip()
            )

        except Error as error:
            connection.rollback()
            print(f"Error adding doctor: {error}")
            return None

        finally:
            cursor.close()
            connection.close()

    # =========================================================
    # GET ALL DOCTORS
    # =========================================================

    def get_all_doctors(self):
        """Return all doctors."""

        connection = self.database_manager.get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)

        try:
            sql = """
                SELECT
                    doctor_id,
                    user_id,
                    first_name,
                    last_name,
                    specialization,
                    phone,
                    email
                FROM doctors
                ORDER BY doctor_id DESC
            """

            cursor.execute(sql)

            rows = cursor.fetchall()

            doctors = []

            for row in rows:
                doctors.append(
                    Doctor(
                        doctor_id=row["doctor_id"],
                        user_id=row.get("user_id"),
                        first_name=row["first_name"],
                        last_name=row["last_name"],
                        specialization=row["specialization"] or "",
                        phone=row["phone"] or "",
                        email=row["email"] or ""
                    )
                )

            return doctors

        except Error as error:
            print(f"Error getting doctors: {error}")
            return []

        finally:
            cursor.close()
            connection.close()

    # =========================================================
    # GET ONE DOCTOR
    # =========================================================

    def get_doctor(self, doctor_id):
        """Return one doctor by ID."""

        connection = self.database_manager.get_connection()

        if connection is None:
            return None

        cursor = connection.cursor(dictionary=True)

        try:
            sql = """
                SELECT
                    doctor_id,
                    user_id,
                    first_name,
                    last_name,
                    specialization,
                    phone,
                    email
                FROM doctors
                WHERE doctor_id = %s
            """

            cursor.execute(sql, (doctor_id,))

            row = cursor.fetchone()

            if row is None:
                return None

            return Doctor(
                doctor_id=row["doctor_id"],
                user_id=row.get("user_id"),
                first_name=row["first_name"],
                last_name=row["last_name"],
                specialization=row["specialization"] or "",
                phone=row["phone"] or "",
                email=row["email"] or ""
            )

        except Error as error:
            print(f"Error getting doctor: {error}")
            return None

        finally:
            cursor.close()
            connection.close()

    # =========================================================
    # UPDATE DOCTOR
    # =========================================================

    def update_doctor(
        self,
        doctor_id,
        first_name,
        last_name,
        specialization="",
        phone="",
        email=""
    ):
        """Update an existing doctor."""

        connection = self.database_manager.get_connection()

        if connection is None:
            return False

        cursor = connection.cursor()

        try:
            sql = """
                UPDATE doctors
                SET
                    first_name = %s,
                    last_name = %s,
                    specialization = %s,
                    phone = %s,
                    email = %s
                WHERE doctor_id = %s
            """

            values = (
                first_name.strip(),
                last_name.strip(),
                specialization.strip(),
                phone.strip(),
                email.strip(),
                doctor_id
            )

            cursor.execute(sql, values)
            connection.commit()

            return cursor.rowcount > 0

        except Error as error:
            connection.rollback()
            print(f"Error updating doctor: {error}")
            return False

        finally:
            cursor.close()
            connection.close()

    # =========================================================
    # DELETE DOCTOR
    # =========================================================

    def delete_doctor(self, doctor_id):
        """Delete a doctor by ID."""

        connection = self.database_manager.get_connection()

        if connection is None:
            return False

        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                DELETE FROM doctors
                WHERE doctor_id = %s
                """,
                (doctor_id,)
            )

            connection.commit()

            return cursor.rowcount > 0

        except Error as error:
            connection.rollback()
            print(f"Error deleting doctor: {error}")
            return False

        finally:
            cursor.close()
            connection.close()


if __name__ == "__main__":
    service = DoctorService()

    if service.database_manager.test_connection():
        print("Doctor Service MySQL connection: SUCCESS")
    else:
        print("Doctor Service MySQL connection: FAILED")