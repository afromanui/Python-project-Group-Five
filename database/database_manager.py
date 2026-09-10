import mysql.connector
from mysql.connector import Error


class DatabaseManager:
    """Manages the MySQL database connection and appointment operations."""

    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.database = "hospital_management"

    def get_connection(self):
        """Create and return a connection to the MySQL database."""

        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            if connection.is_connected():
                return connection

        except Error as error:
            print(f"Database connection error: {error}")

        return None

    def test_connection(self):
        """Test the MySQL database connection."""

        connection = self.get_connection()

        if connection:
            print("MySQL connection successful!")
            print(f"Connected to database: {self.database}")
            connection.close()
            return True

        print("MySQL connection failed!")
        return False

    # =========================================================
    # APPOINTMENT CRUD OPERATIONS
    # =========================================================

    def add_appointment(self, appointment):
        """Add a new appointment to the database."""

        connection = self.get_connection()

        if connection is None:
            return None

        cursor = connection.cursor()

        try:
            sql = """
                INSERT INTO appointments
                (
                    patient_id,
                    doctor_id,
                    appointment_date,
                    appointment_time,
                    reason,
                    status
                )
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            values = (
                appointment.patient_id,
                appointment.doctor_id,
                appointment.appointment_date,
                appointment.appointment_time,
                appointment.reason,
                appointment.status
            )

            cursor.execute(sql, values)
            connection.commit()

            # MySQL automatically creates the appointment ID
            appointment.appointment_id = cursor.lastrowid

            print(
                f"Appointment added successfully. "
                f"Appointment ID: {appointment.appointment_id}"
            )

            return appointment.appointment_id

        except Error as error:
            connection.rollback()
            print(f"Error adding appointment: {error}")
            return None

        finally:
            cursor.close()
            connection.close()

    def get_appointments(self):
        """Get all appointments from the database."""

        connection = self.get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)

        try:
            sql = """
                SELECT
                    appointment_id,
                    patient_id,
                    doctor_id,
                    appointment_date,
                    appointment_time,
                    reason,
                    status,
                    created_at
                FROM appointments
                ORDER BY appointment_id
            """

            cursor.execute(sql)

            return cursor.fetchall()

        except Error as error:
            print(f"Error getting appointments: {error}")
            return []

        finally:
            cursor.close()
            connection.close()

    def get_appointment(self, appointment_id):
        """Get one appointment by ID."""

        connection = self.get_connection()

        if connection is None:
            return None

        cursor = connection.cursor(dictionary=True)

        try:
            sql = """
                SELECT
                    appointment_id,
                    patient_id,
                    doctor_id,
                    appointment_date,
                    appointment_time,
                    reason,
                    status,
                    created_at
                FROM appointments
                WHERE appointment_id = %s
            """

            cursor.execute(sql, (appointment_id,))

            return cursor.fetchone()

        except Error as error:
            print(f"Error getting appointment: {error}")
            return None

        finally:
            cursor.close()
            connection.close()

    def update_appointment(self, appointment):
        """Update an existing appointment."""

        connection = self.get_connection()

        if connection is None:
            return False

        cursor = connection.cursor()

        try:
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
                appointment.patient_id,
                appointment.doctor_id,
                appointment.appointment_date,
                appointment.appointment_time,
                appointment.reason,
                appointment.status,
                appointment.appointment_id
            )

            cursor.execute(sql, values)
            connection.commit()

            print(
                f"Appointment {appointment.appointment_id} "
                f"updated successfully."
            )

            return cursor.rowcount > 0

        except Error as error:
            connection.rollback()
            print(f"Error updating appointment: {error}")
            return False

        finally:
            cursor.close()
            connection.close()

    def delete_appointment(self, appointment_id):
        """Delete an appointment by ID."""

        connection = self.get_connection()

        if connection is None:
            return False

        cursor = connection.cursor()

        try:
            sql = """
                DELETE FROM appointments
                WHERE appointment_id = %s
            """

            cursor.execute(sql, (appointment_id,))
            connection.commit()

            if cursor.rowcount > 0:
                print(
                    f"Appointment {appointment_id} "
                    f"deleted successfully."
                )
                return True

            print(f"Appointment {appointment_id} not found.")
            return False

        except Error as error:
            connection.rollback()
            print(f"Error deleting appointment: {error}")
            return False

        finally:
            cursor.close()
            connection.close()


if __name__ == "__main__":
    database_manager = DatabaseManager()
    database_manager.test_connection()