import mysql.connector
from mysql.connector import Error

from database.database_manager import DatabaseManager
from models.bill import Bill


class BillingService:
    """Handles billing operations using MySQL."""

    VALID_STATUSES = ["Unpaid", "Paid", "Cancelled"]

    def __init__(self):
        self.database_manager = DatabaseManager()

    # ============================================================
    # ADD BILL
    # ============================================================

    def add_bill(
        self,
        patient_id,
        appointment_id=None,
        amount=0.0,
        description="",
        status="Unpaid"
    ):
        connection = self.database_manager.get_connection()

        if connection is None:
            print("Database connection failed.")
            return None

        cursor = connection.cursor()

        try:
            # Validate patient ID
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

            # Validate appointment ID if supplied
            if appointment_id is not None:
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

            # Validate amount
            try:
                amount = float(amount)
            except (TypeError, ValueError):
                print("Amount must be a valid number.")
                return None

            if amount < 0:
                print("Amount cannot be negative.")
                return None

            # Validate status
            if status not in self.VALID_STATUSES:
                print("Invalid payment status.")
                return None

            # Insert bill
            sql = """
                INSERT INTO bills (
                    patient_id,
                    appointment_id,
                    amount,
                    description,
                    status
                )
                VALUES (%s, %s, %s, %s, %s)
            """

            values = (
                patient_id,
                appointment_id,
                amount,
                description,
                status
            )

            cursor.execute(sql, values)
            connection.commit()

            bill_id = cursor.lastrowid

            print(
                f"Bill added successfully. Bill ID: {bill_id}"
            )

            return Bill(
                bill_id=bill_id,
                patient_id=patient_id,
                appointment_id=appointment_id,
                amount=amount,
                payment_status=status,
                bill_date=""
            )

        except Error as error:
            connection.rollback()
            print(f"Database error: {error}")
            return None

        finally:
            cursor.close()
            connection.close()

    # ============================================================
    # GET ALL BILLS
    # ============================================================

    def get_all_bills(self):
        connection = self.database_manager.get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)

        try:
            sql = """
                SELECT
                    b.bill_id,
                    b.patient_id,
                    b.appointment_id,
                    b.amount,
                    b.description,
                    b.status,
                    b.payment_date,
                    b.created_at,
                    p.first_name AS patient_first_name,
                    p.last_name AS patient_last_name
                FROM bills b
                JOIN patients p
                    ON b.patient_id = p.patient_id
                ORDER BY b.bill_id DESC
            """

            cursor.execute(sql)

            return cursor.fetchall()

        except Error as error:
            print(f"Database error: {error}")
            return []

        finally:
            cursor.close()
            connection.close()

    # ============================================================
    # GET ONE BILL
    # ============================================================

    def get_bill(self, bill_id):
        connection = self.database_manager.get_connection()

        if connection is None:
            return None

        cursor = connection.cursor(dictionary=True)

        try:
            sql = """
                SELECT
                    b.bill_id,
                    b.patient_id,
                    b.appointment_id,
                    b.amount,
                    b.description,
                    b.status,
                    b.payment_date,
                    b.created_at,
                    p.first_name AS patient_first_name,
                    p.last_name AS patient_last_name
                FROM bills b
                JOIN patients p
                    ON b.patient_id = p.patient_id
                WHERE b.bill_id = %s
            """

            cursor.execute(sql, (bill_id,))

            return cursor.fetchone()

        except Error as error:
            print(f"Database error: {error}")
            return None

        finally:
            cursor.close()
            connection.close()

    # ============================================================
    # UPDATE BILL
    # ============================================================

    def update_bill(
        self,
        bill_id,
        patient_id,
        appointment_id=None,
        amount=0.0,
        description="",
        status="Unpaid"
    ):
        connection = self.database_manager.get_connection()

        if connection is None:
            return False

        cursor = connection.cursor()

        try:
            # Check bill exists
            cursor.execute(
                """
                SELECT bill_id
                FROM bills
                WHERE bill_id = %s
                """,
                (bill_id,)
            )

            if cursor.fetchone() is None:
                print(f"Bill {bill_id} not found.")
                return False

            # Check patient exists
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

            # Check appointment exists if supplied
            if appointment_id is not None:
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

            # Validate amount
            try:
                amount = float(amount)
            except (TypeError, ValueError):
                print("Amount must be a valid number.")
                return False

            if amount < 0:
                print("Amount cannot be negative.")
                return False

            # Validate status
            if status not in self.VALID_STATUSES:
                print("Invalid payment status.")
                return False

            # Update payment date automatically
            if status == "Paid":
                sql = """
                    UPDATE bills
                    SET
                        patient_id = %s,
                        appointment_id = %s,
                        amount = %s,
                        description = %s,
                        status = %s,
                        payment_date = CURRENT_TIMESTAMP
                    WHERE bill_id = %s
                """

                values = (
                    patient_id,
                    appointment_id,
                    amount,
                    description,
                    status,
                    bill_id
                )

            else:
                sql = """
                    UPDATE bills
                    SET
                        patient_id = %s,
                        appointment_id = %s,
                        amount = %s,
                        description = %s,
                        status = %s,
                        payment_date = NULL
                    WHERE bill_id = %s
                """

                values = (
                    patient_id,
                    appointment_id,
                    amount,
                    description,
                    status,
                    bill_id
                )

            cursor.execute(sql, values)
            connection.commit()

            print(
                f"Bill {bill_id} updated successfully."
            )

            return True

        except Error as error:
            connection.rollback()
            print(f"Database error: {error}")
            return False

        finally:
            cursor.close()
            connection.close()

    # ============================================================
    # UPDATE BILL STATUS
    # ============================================================

    def update_bill_status(self, bill_id, status):
        connection = self.database_manager.get_connection()

        if connection is None:
            return False

        cursor = connection.cursor()

        try:
            if status not in self.VALID_STATUSES:
                print("Invalid payment status.")
                return False

            # Check bill exists first
            cursor.execute(
                """
                SELECT bill_id
                FROM bills
                WHERE bill_id = %s
                """,
                (bill_id,)
            )

            if cursor.fetchone() is None:
                print(f"Bill {bill_id} not found.")
                return False

            if status == "Paid":
                sql = """
                    UPDATE bills
                    SET
                        status = %s,
                        payment_date = CURRENT_TIMESTAMP
                    WHERE bill_id = %s
                """

                values = (status, bill_id)

            else:
                sql = """
                    UPDATE bills
                    SET
                        status = %s,
                        payment_date = NULL
                    WHERE bill_id = %s
                """

                values = (status, bill_id)

            cursor.execute(sql, values)
            connection.commit()

            print(
                f"Bill {bill_id} status updated to {status}."
            )

            return True

        except Error as error:
            connection.rollback()
            print(f"Database error: {error}")
            return False

        finally:
            cursor.close()
            connection.close()

    # ============================================================
    # DELETE BILL
    # ============================================================

    def delete_bill(self, bill_id):
        connection = self.database_manager.get_connection()

        if connection is None:
            return False

        cursor = connection.cursor()

        try:
            # Check bill exists
            cursor.execute(
                """
                SELECT bill_id
                FROM bills
                WHERE bill_id = %s
                """,
                (bill_id,)
            )

            if cursor.fetchone() is None:
                print(f"Bill {bill_id} not found.")
                return False

            # Delete
            cursor.execute(
                """
                DELETE FROM bills
                WHERE bill_id = %s
                """,
                (bill_id,)
            )

            connection.commit()

            print(
                f"Bill {bill_id} deleted successfully."
            )

            return True

        except Error as error:
            connection.rollback()
            print(f"Database error: {error}")
            return False

        finally:
            cursor.close()
            connection.close()


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":
    print("Billing Service loaded successfully")

    service = BillingService()

    connection = service.database_manager.get_connection()

    if connection:
        print("Billing Service MySQL connection: SUCCESS")
        connection.close()
    else:
        print("Billing Service MySQL connection: FAILED")