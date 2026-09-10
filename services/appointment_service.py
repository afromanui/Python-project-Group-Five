from database.database_manager import DatabaseManager
from models.appointment import Appointment


class AppointmentService:
    """Handles appointment database operations using MySQL."""

    ALLOWED_STATUSES = {
        "Scheduled",
        "Completed",
        "Cancelled"
    }

    def __init__(self):
        self.database_manager = DatabaseManager()

    # =========================================================
    # ADD APPOINTMENT
    # =========================================================

    def add_appointment(
        self,
        patient_id,
        doctor_id,
        appointment_date,
        appointment_time,
        reason="",
        status="Scheduled"
    ):
        """Add a new appointment."""

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

            # Validate status
            if status not in self.ALLOWED_STATUSES:
                status = "Scheduled"

            appointment = Appointment(
                patient_id=patient_id,
                doctor_id=doctor_id,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                reason=reason,
                status=status
            )

            appointment_id = (
                self.database_manager.add_appointment(appointment)
            )

            if appointment_id:
                appointment.appointment_id = appointment_id
                return appointment

            return None

        except Exception as error:
            print(f"Error adding appointment: {error}")

            try:
                connection.rollback()
            except Exception:
                pass

            return None

        finally:
            cursor.close()
            connection.close()

    # =========================================================
    # GET ALL APPOINTMENTS
    # =========================================================

    def get_all_appointments(self):
        """Return all appointments with patient and doctor names."""

        connection = self.database_manager.get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)

        try:
            sql = """
                SELECT
                    a.appointment_id,
                    a.patient_id,
                    a.doctor_id,
                    a.appointment_date,
                    a.appointment_time,
                    a.reason,
                    a.status,
                    a.created_at,

                    p.first_name AS patient_first_name,
                    p.last_name AS patient_last_name,

                    d.first_name AS doctor_first_name,
                    d.last_name AS doctor_last_name

                FROM appointments a

                JOIN patients p
                    ON a.patient_id = p.patient_id

                JOIN doctors d
                    ON a.doctor_id = d.doctor_id

                ORDER BY
                    a.appointment_date ASC,
                    a.appointment_time ASC
            """

            cursor.execute(sql)

            return cursor.fetchall()

        except Exception as error:
            print(f"Error getting appointments: {error}")
            return []

        finally:
            cursor.close()
            connection.close()

    # =========================================================
    # GET ONE APPOINTMENT
    # =========================================================

    def get_appointment(self, appointment_id):
        """Find an appointment by ID."""

        connection = self.database_manager.get_connection()

        if connection is None:
            return None

        cursor = connection.cursor(dictionary=True)

        try:
            sql = """
                SELECT
                    a.appointment_id,
                    a.patient_id,
                    a.doctor_id,
                    a.appointment_date,
                    a.appointment_time,
                    a.reason,
                    a.status,
                    a.created_at,

                    p.first_name AS patient_first_name,
                    p.last_name AS patient_last_name,

                    d.first_name AS doctor_first_name,
                    d.last_name AS doctor_last_name

                FROM appointments a

                JOIN patients p
                    ON a.patient_id = p.patient_id

                JOIN doctors d
                    ON a.doctor_id = d.doctor_id

                WHERE a.appointment_id = %s
            """

            cursor.execute(sql, (appointment_id,))

            return cursor.fetchone()

        except Exception as error:
            print(f"Error getting appointment: {error}")
            return None

        finally:
            cursor.close()
            connection.close()

    # =========================================================
    # UPDATE APPOINTMENT
    # =========================================================

    def update_appointment(
        self,
        appointment_id,
        patient_id,
        doctor_id,
        appointment_date,
        appointment_time,
        reason="",
        status="Scheduled"
    ):
        """Update an existing appointment."""

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

            # Validate status
            if status not in self.ALLOWED_STATUSES:
                print("Invalid appointment status.")
                return False

            sql = """
                UPDATE appointments
                SET
                    patient_id = %s,
                    doctor_id = %s,
                    appointment_date = %s,
                    appointment_time = %s,
                    reason = %s,
                    status = %s
                WHERE appointment_id = %s
            """

            values = (
                patient_id,
                doctor_id,
                appointment_date,
                appointment_time,
                reason,
                status,
                appointment_id
            )

            cursor.execute(sql, values)
            connection.commit()

            return cursor.rowcount > 0

        except Exception as error:
            connection.rollback()
            print(f"Error updating appointment: {error}")
            return False

        finally:
            cursor.close()
            connection.close()

    # =========================================================
    # UPDATE STATUS ONLY
    # =========================================================

    def update_status(self, appointment_id, status):
        """Update appointment status only."""

        if status not in self.ALLOWED_STATUSES:
            print("Invalid appointment status.")
            return False

        connection = self.database_manager.get_connection()

        if connection is None:
            return False

        cursor = connection.cursor()

        try:
            sql = """
                UPDATE appointments
                SET status = %s
                WHERE appointment_id = %s
            """

            cursor.execute(
                sql,
                (status, appointment_id)
            )

            connection.commit()

            return cursor.rowcount > 0

        except Exception as error:
            connection.rollback()
            print(f"Error updating appointment status: {error}")
            return False

        finally:
            cursor.close()
            connection.close()

    # =========================================================
    # DELETE APPOINTMENT
    # =========================================================

    def delete_appointment(self, appointment_id):
        """Delete an appointment."""

        connection = self.database_manager.get_connection()

        if connection is None:
            return False

        cursor = connection.cursor()

        try:
            sql = """
                DELETE FROM appointments
                WHERE appointment_id = %s
            """

            cursor.execute(
                sql,
                (appointment_id,)
            )

            connection.commit()

            return cursor.rowcount > 0

        except Exception as error:
            connection.rollback()
            print(f"Error deleting appointment: {error}")
            return False

        finally:
            cursor.close()
            connection.close()


# =============================================================
# TEST APPOINTMENT SERVICE
# =============================================================

if __name__ == "__main__":

    service = AppointmentService()

    connection = service.database_manager.get_connection()

    if connection:
        print("Appointment Service MySQL connection: SUCCESS")
        connection.close()
    else:
        print("Appointment Service MySQL connection: FAILED")