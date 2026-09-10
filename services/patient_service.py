import mysql.connector
from mysql.connector import Error

from database.database_manager import DatabaseManager
from models.patient import Patient


class PatientService:
    """Handles patient database operations using MySQL."""

    def __init__(self):
        self.database_manager = DatabaseManager()

    # =========================================================
    # ADD PATIENT
    # =========================================================

    def add_patient(
        self,
        first_name,
        last_name,
        date_of_birth="",
        gender="",
        phone="",
        address="",
        emergency_contact=""
    ):
        """Add a new patient."""

        connection = self.database_manager.get_connection()

        if connection is None:
            return None

        cursor = connection.cursor()

        try:
            sql = """
                INSERT INTO patients
                (
                    first_name,
                    last_name,
                    date_of_birth,
                    gender,
                    phone,
                    address,
                    emergency_contact
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            values = (
                first_name.strip(),
                last_name.strip(),
                date_of_birth.strip(),
                gender.strip(),
                phone.strip(),
                address.strip(),
                emergency_contact.strip()
            )

            cursor.execute(sql, values)
            connection.commit()

            patient_id = cursor.lastrowid

            return Patient(
                patient_id=patient_id,
                first_name=first_name.strip(),
                last_name=last_name.strip(),
                date_of_birth=date_of_birth.strip(),
                gender=gender.strip(),
                phone=phone.strip(),
                address=address.strip(),
                emergency_contact=emergency_contact.strip()
            )

        except Error as error:
            connection.rollback()
            print(f"Error adding patient: {error}")
            return None

        finally:
            cursor.close()
            connection.close()

    # =========================================================
    # GET ALL PATIENTS
    # =========================================================

    def get_all_patients(self):
        """Return all patients."""

        connection = self.database_manager.get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)

        try:
            sql = """
                SELECT
                    patient_id,
                    first_name,
                    last_name,
                    date_of_birth,
                    gender,
                    phone,
                    address,
                    emergency_contact
                FROM patients
                ORDER BY patient_id DESC
            """

            cursor.execute(sql)

            rows = cursor.fetchall()

            patients = []

            for row in rows:
                patients.append(
                    Patient(
                        patient_id=row["patient_id"],
                        first_name=row["first_name"],
                        last_name=row["last_name"],
                        date_of_birth=row["date_of_birth"] or "",
                        gender=row["gender"] or "",
                        phone=row["phone"] or "",
                        address=row["address"] or "",
                        emergency_contact=row["emergency_contact"] or ""
                    )
                )

            return patients

        except Error as error:
            print(f"Error getting patients: {error}")
            return []

        finally:
            cursor.close()
            connection.close()

    # =========================================================
    # GET ONE PATIENT
    # =========================================================

    def get_patient(self, patient_id):
        """Return one patient by ID."""

        connection = self.database_manager.get_connection()

        if connection is None:
            return None

        cursor = connection.cursor(dictionary=True)

        try:
            sql = """
                SELECT
                    patient_id,
                    first_name,
                    last_name,
                    date_of_birth,
                    gender,
                    phone,
                    address,
                    emergency_contact
                FROM patients
                WHERE patient_id = %s
            """

            cursor.execute(sql, (patient_id,))

            row = cursor.fetchone()

            if row is None:
                return None

            return Patient(
                patient_id=row["patient_id"],
                first_name=row["first_name"],
                last_name=row["last_name"],
                date_of_birth=row["date_of_birth"] or "",
                gender=row["gender"] or "",
                phone=row["phone"] or "",
                address=row["address"] or "",
                emergency_contact=row["emergency_contact"] or ""
            )

        except Error as error:
            print(f"Error getting patient: {error}")
            return None

        finally:
            cursor.close()
            connection.close()

    # =========================================================
    # UPDATE PATIENT
    # =========================================================

    def update_patient(
        self,
        patient_id,
        first_name,
        last_name,
        date_of_birth="",
        gender="",
        phone="",
        address="",
        emergency_contact=""
    ):
        """Update an existing patient."""

        connection = self.database_manager.get_connection()

        if connection is None:
            return False

        cursor = connection.cursor()

        try:
            sql = """
                UPDATE patients
                SET
                    first_name = %s,
                    last_name = %s,
                    date_of_birth = %s,
                    gender = %s,
                    phone = %s,
                    address = %s,
                    emergency_contact = %s
                WHERE patient_id = %s
            """

            values = (
                first_name.strip(),
                last_name.strip(),
                date_of_birth.strip(),
                gender.strip(),
                phone.strip(),
                address.strip(),
                emergency_contact.strip(),
                patient_id
            )

            cursor.execute(sql, values)
            connection.commit()

            return cursor.rowcount > 0

        except Error as error:
            connection.rollback()
            print(f"Error updating patient: {error}")
            return False

        finally:
            cursor.close()
            connection.close()

    # =========================================================
    # DELETE PATIENT
    # =========================================================

    def delete_patient(self, patient_id):
        """Delete a patient by ID."""

        connection = self.database_manager.get_connection()

        if connection is None:
            return False

        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                DELETE FROM patients
                WHERE patient_id = %s
                """,
                (patient_id,)
            )

            connection.commit()

            return cursor.rowcount > 0

        except Error as error:
            connection.rollback()
            print(f"Error deleting patient: {error}")
            return False

        finally:
            cursor.close()
            connection.close()


if __name__ == "__main__":
    service = PatientService()

    if service.database_manager.test_connection():
        print("Patient Service MySQL connection: SUCCESS")
    else:
        print("Patient Service MySQL connection: FAILED")