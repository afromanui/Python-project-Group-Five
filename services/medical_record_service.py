from mysql.connector import Error

from database.database_manager import DatabaseManager
from models.medical_record import MedicalRecord


class MedicalRecordService:
    """Handles medical record operations using MySQL."""

    def __init__(self):
        self.database_manager = DatabaseManager()

    # =========================================================
    # ADD MEDICAL RECORD
    # =========================================================

    def add_medical_record(
        self,
        patient_id,
        doctor_id,
        appointment_id=None,
        diagnosis="",
        treatment="",
        notes=""
    ):
        """Add a new medical record."""

        connection = self.database_manager.get_connection()

        if connection is None:
            print("Database connection failed.")
            return None

        cursor = connection.cursor()

        try:
            # Check patient
            cursor.execute(
                """
                SELECT patient_id
                FROM patients
                WHERE patient_id = %s
                """,
                (patient_id,)
            )

            if cursor.fetchone() is None:
                print("Patient ID does not exist.")
                return None

            # Check doctor
            cursor.execute(
                """
                SELECT doctor_id
                FROM doctors
                WHERE doctor_id = %s
                """,
                (doctor_id,)
            )

            if cursor.fetchone() is None:
                print("Doctor ID does not exist.")
                return None

            # Check appointment if supplied
            if appointment_id not in (None, ""):
                cursor.execute(
                    """
                    SELECT appointment_id
                    FROM appointments
                    WHERE appointment_id = %s
                    """,
                    (appointment_id,)
                )

                if cursor.fetchone() is None:
                    print("Appointment ID does not exist.")
                    return None

            # Empty appointment ID becomes NULL
            if appointment_id == "":
                appointment_id = None

            sql = """
                INSERT INTO medical_records (
                    patient_id,
                    doctor_id,
                    appointment_id,
                    diagnosis,
                    treatment,
                    notes
                )
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            values = (
                patient_id,
                doctor_id,
                appointment_id,
                diagnosis.strip(),
                treatment.strip(),
                notes.strip()
            )

            cursor.execute(sql, values)
            connection.commit()

            record_id = cursor.lastrowid

            return MedicalRecord(
                record_id=record_id,
                patient_id=patient_id,
                doctor_id=doctor_id,
                diagnosis=diagnosis.strip(),
                treatment=treatment.strip(),
                prescription=notes.strip(),
                record_date=""
            )

        except Error as error:
            connection.rollback()
            print(f"Database error adding medical record: {error}")
            return None

        finally:
            cursor.close()
            connection.close()

    # =========================================================
    # GET ALL MEDICAL RECORDS
    # =========================================================

    def get_all_medical_records(self):
        """Return all medical records with patient and doctor names."""

        connection = self.database_manager.get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)

        try:
            sql = """
                SELECT
                    mr.record_id,
                    mr.patient_id,
                    mr.doctor_id,
                    mr.appointment_id,
                    mr.diagnosis,
                    mr.treatment,
                    mr.notes,
                    mr.created_at,

                    p.first_name AS patient_first_name,
                    p.last_name AS patient_last_name,

                    d.first_name AS doctor_first_name,
                    d.last_name AS doctor_last_name

                FROM medical_records mr

                JOIN patients p
                    ON mr.patient_id = p.patient_id

                JOIN doctors d
                    ON mr.doctor_id = d.doctor_id

                ORDER BY mr.record_id DESC
            """

            cursor.execute(sql)

            return cursor.fetchall()

        except Error as error:
            print(f"Database error getting medical records: {error}")
            return []

        finally:
            cursor.close()
            connection.close()

    # =========================================================
    # GET ONE MEDICAL RECORD
    # =========================================================

    def get_medical_record(self, record_id):
        """Find one medical record by ID."""

        connection = self.database_manager.get_connection()

        if connection is None:
            return None

        cursor = connection.cursor(dictionary=True)

        try:
            sql = """
                SELECT
                    mr.record_id,
                    mr.patient_id,
                    mr.doctor_id,
                    mr.appointment_id,
                    mr.diagnosis,
                    mr.treatment,
                    mr.notes,
                    mr.created_at,

                    p.first_name AS patient_first_name,
                    p.last_name AS patient_last_name,

                    d.first_name AS doctor_first_name,
                    d.last_name AS doctor_last_name

                FROM medical_records mr

                JOIN patients p
                    ON mr.patient_id = p.patient_id

                JOIN doctors d
                    ON mr.doctor_id = d.doctor_id

                WHERE mr.record_id = %s
            """

            cursor.execute(sql, (record_id,))

            return cursor.fetchone()

        except Error as error:
            print(f"Database error getting medical record: {error}")
            return None

        finally:
            cursor.close()
            connection.close()

    # =========================================================
    # UPDATE MEDICAL RECORD
    # =========================================================

    def update_medical_record(
        self,
        record_id,
        patient_id,
        doctor_id,
        appointment_id=None,
        diagnosis="",
        treatment="",
        notes=""
    ):
        """Update an existing medical record."""

        connection = self.database_manager.get_connection()

        if connection is None:
            return False

        cursor = connection.cursor()

        try:
            # Check patient
            cursor.execute(
                """
                SELECT patient_id
                FROM patients
                WHERE patient_id = %s
                """,
                (patient_id,)
            )

            if cursor.fetchone() is None:
                print("Patient ID does not exist.")
                return False

            # Check doctor
            cursor.execute(
                """
                SELECT doctor_id
                FROM doctors
                WHERE doctor_id = %s
                """,
                (doctor_id,)
            )

            if cursor.fetchone() is None:
                print("Doctor ID does not exist.")
                return False

            # Validate appointment when supplied
            if appointment_id not in (None, ""):
                cursor.execute(
                    """
                    SELECT appointment_id
                    FROM appointments
                    WHERE appointment_id = %s
                    """,
                    (appointment_id,)
                )

                if cursor.fetchone() is None:
                    print("Appointment ID does not exist.")
                    return False

            if appointment_id == "":
                appointment_id = None

            sql = """
                UPDATE medical_records
                SET
                    patient_id = %s,
                    doctor_id = %s,
                    appointment_id = %s,
                    diagnosis = %s,
                    treatment = %s,
                    notes = %s
                WHERE record_id = %s
            """

            values = (
                patient_id,
                doctor_id,
                appointment_id,
                diagnosis.strip(),
                treatment.strip(),
                notes.strip(),
                record_id
            )

            cursor.execute(sql, values)
            connection.commit()

            return cursor.rowcount > 0

        except Error as error:
            connection.rollback()
            print(f"Database error updating medical record: {error}")
            return False

        finally:
            cursor.close()
            connection.close()

    # =========================================================
    # DELETE MEDICAL RECORD
    # =========================================================

    def delete_medical_record(self, record_id):
        """Delete a medical record."""

        connection = self.database_manager.get_connection()

        if connection is None:
            return False

        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                DELETE FROM medical_records
                WHERE record_id = %s
                """,
                (record_id,)
            )

            connection.commit()

            return cursor.rowcount > 0

        except Error as error:
            connection.rollback()
            print(f"Database error deleting medical record: {error}")
            return False

        finally:
            cursor.close()
            connection.close()


# =============================================================
# TEST MEDICAL RECORD SERVICE
# =============================================================

if __name__ == "__main__":

    service = MedicalRecordService()

    connection = service.database_manager.get_connection()

    if connection:
        print("Medical Record Service MySQL connection: SUCCESS")
        connection.close()
    else:
        print("Medical Record Service MySQL connection: FAILED")