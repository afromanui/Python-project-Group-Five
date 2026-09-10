from database.database_manager import DatabaseManager

from services.patient_service import PatientService
from services.doctor_service import DoctorService
from services.appointment_service import AppointmentService
from services.medical_record_service import MedicalRecordService
from services.billing_service import BillingService
from services.administrator_service import AdministratorService


# ============================================================
# PATIENT MANAGEMENT
# ============================================================

def patient_menu():
    patient_service = PatientService()

    while True:
        print("\n" + "=" * 50)
        print("           PATIENT MANAGEMENT")
        print("=" * 50)
        print("1. Add Patient")
        print("2. View All Patients")
        print("3. Search Patient")
        print("4. Delete Patient")
        print("5. Back to Main Menu")
        print("=" * 50)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            print("\n--- Add New Patient ---")

            first_name = input("First name: ").strip()
            last_name = input("Last name: ").strip()
            date_of_birth = input(
                "Date of birth (YYYY-MM-DD): "
            ).strip()
            gender = input(
                "Gender (Male/Female/Other): "
            ).strip()
            phone = input("Phone: ").strip()
            address = input("Address: ").strip()
            emergency_contact = input(
                "Emergency contact: "
            ).strip()

            if not first_name or not last_name:
                print("\nFirst name and last name are required.")
                continue

            patient = patient_service.add_patient(
                first_name,
                last_name,
                date_of_birth,
                gender,
                phone,
                address,
                emergency_contact
            )

            if patient:
                print("\nPatient added successfully!")
                print(patient)
            else:
                print("\nFailed to add patient.")

        elif choice == "2":
            print("\n--- All Patients ---")

            patients = patient_service.get_all_patients()

            if not patients:
                print("No patients found.")
                continue

            for patient in patients:
                print(f"\nID: {patient.patient_id}")
                print(
                    f"Name: "
                    f"{patient.first_name} {patient.last_name}"
                )
                print(
                    f"Date of Birth: "
                    f"{patient.date_of_birth}"
                )
                print(f"Gender: {patient.gender}")
                print(f"Phone: {patient.phone}")
                print(f"Address: {patient.address}")
                print(
                    f"Emergency Contact: "
                    f"{patient.emergency_contact}"
                )
                print("-" * 40)

        elif choice == "3":
            print("\n--- Search Patient ---")

            try:
                patient_id = int(
                    input("Enter patient ID: ").strip()
                )
            except ValueError:
                print("\nPlease enter a valid numeric patient ID.")
                continue

            patient = patient_service.get_patient(patient_id)

            if patient:
                print("\nPatient found:")
                print(f"ID: {patient.patient_id}")
                print(
                    f"Name: "
                    f"{patient.first_name} {patient.last_name}"
                )
                print(
                    f"Date of Birth: "
                    f"{patient.date_of_birth}"
                )
                print(f"Gender: {patient.gender}")
                print(f"Phone: {patient.phone}")
                print(f"Address: {patient.address}")
                print(
                    f"Emergency Contact: "
                    f"{patient.emergency_contact}"
                )
            else:
                print("\nPatient not found.")

        elif choice == "4":
            print("\n--- Delete Patient ---")

            try:
                patient_id = int(
                    input("Enter patient ID: ").strip()
                )
            except ValueError:
                print("\nPlease enter a valid numeric patient ID.")
                continue

            patient = patient_service.get_patient(patient_id)

            if not patient:
                print("\nPatient not found.")
                continue

            print(
                f"\nPatient: "
                f"{patient.first_name} {patient.last_name}"
            )

            confirmation = input(
                "Are you sure you want to delete this patient? (y/n): "
            ).strip().lower()

            if confirmation == "y":
                if patient_service.delete_patient(patient_id):
                    print("\nPatient deleted successfully.")
                else:
                    print("\nFailed to delete patient.")
            else:
                print("\nDelete cancelled.")

        elif choice == "5":
            break

        else:
            print("\nInvalid choice. Please enter 1-5.")


# ============================================================
# DOCTOR MANAGEMENT
# ============================================================

def doctor_menu():
    doctor_service = DoctorService()

    while True:
        print("\n" + "=" * 50)
        print("            DOCTOR MANAGEMENT")
        print("=" * 50)
        print("1. Add Doctor")
        print("2. View All Doctors")
        print("3. Search Doctor")
        print("4. Delete Doctor")
        print("5. Back to Main Menu")
        print("=" * 50)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            print("\n--- Add New Doctor ---")

            first_name = input("First name: ").strip()
            last_name = input("Last name: ").strip()
            specialization = input(
                "Specialization: "
            ).strip()
            phone = input("Phone: ").strip()
            email = input("Email: ").strip()

            if not first_name or not last_name:
                print("\nFirst name and last name are required.")
                continue

            doctor = doctor_service.add_doctor(
                first_name,
                last_name,
                specialization,
                phone,
                email
            )

            if doctor:
                print("\nDoctor added successfully!")
                print(doctor)
            else:
                print("\nFailed to add doctor.")

        elif choice == "2":
            print("\n--- All Doctors ---")

            doctors = doctor_service.get_all_doctors()

            if not doctors:
                print("No doctors found.")
                continue

            for doctor in doctors:
                print(f"\nID: {doctor.doctor_id}")
                print(
                    f"Name: "
                    f"{doctor.first_name} {doctor.last_name}"
                )
                print(
                    f"Specialization: "
                    f"{doctor.specialization}"
                )
                print(f"Phone: {doctor.phone}")
                print(f"Email: {doctor.email}")
                print("-" * 40)

        elif choice == "3":
            print("\n--- Search Doctor ---")

            try:
                doctor_id = int(
                    input("Enter doctor ID: ").strip()
                )
            except ValueError:
                print("\nPlease enter a valid numeric doctor ID.")
                continue

            doctor = doctor_service.get_doctor(doctor_id)

            if doctor:
                print("\nDoctor found:")
                print(f"ID: {doctor.doctor_id}")
                print(
                    f"Name: "
                    f"{doctor.first_name} {doctor.last_name}"
                )
                print(
                    f"Specialization: "
                    f"{doctor.specialization}"
                )
                print(f"Phone: {doctor.phone}")
                print(f"Email: {doctor.email}")
            else:
                print("\nDoctor not found.")

        elif choice == "4":
            print("\n--- Delete Doctor ---")

            try:
                doctor_id = int(
                    input("Enter doctor ID: ").strip()
                )
            except ValueError:
                print("\nPlease enter a valid numeric doctor ID.")
                continue

            doctor = doctor_service.get_doctor(doctor_id)

            if not doctor:
                print("\nDoctor not found.")
                continue

            print(
                f"\nDoctor: "
                f"{doctor.first_name} {doctor.last_name}"
            )

            confirmation = input(
                "Are you sure you want to delete this doctor? (y/n): "
            ).strip().lower()

            if confirmation == "y":
                if doctor_service.delete_doctor(doctor_id):
                    print("\nDoctor deleted successfully.")
                else:
                    print("\nFailed to delete doctor.")
            else:
                print("\nDelete cancelled.")

        elif choice == "5":
            break

        else:
            print("\nInvalid choice. Please enter 1-5.")


# ============================================================
# APPOINTMENT MANAGEMENT
# ============================================================

def appointment_menu():
    appointment_service = AppointmentService()

    while True:
        print("\n" + "=" * 50)
        print("         APPOINTMENT MANAGEMENT")
        print("=" * 50)
        print("1. Add Appointment")
        print("2. View All Appointments")
        print("3. Search Appointment")
        print("4. Update Appointment Status")
        print("5. Delete Appointment")
        print("6. Back to Main Menu")
        print("=" * 50)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            print("\n--- Add New Appointment ---")

            try:
                patient_id = int(
                    input("Patient ID: ").strip()
                )
                doctor_id = int(
                    input("Doctor ID: ").strip()
                )
            except ValueError:
                print(
                    "\nPatient ID and Doctor ID must be numbers."
                )
                continue

            appointment_date = input(
                "Appointment date (YYYY-MM-DD): "
            ).strip()

            appointment_time = input(
                "Appointment time (HH:MM): "
            ).strip()

            reason = input(
                "Reason for appointment: "
            ).strip()

            if not appointment_date or not appointment_time:
                print("\nDate and time are required.")
                continue

            appointment = appointment_service.add_appointment(
                patient_id=patient_id,
                doctor_id=doctor_id,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                reason=reason
            )

            if appointment:
                print("\nAppointment added successfully!")
                print(appointment)
            else:
                print("\nFailed to add appointment.")

        elif choice == "2":
            print("\n--- All Appointments ---")

            appointments = (
                appointment_service.get_all_appointments()
            )

            if not appointments:
                print("No appointments found.")
                continue

            for appointment in appointments:
                print(
                    f"\nAppointment ID: "
                    f"{appointment['appointment_id']}"
                )
                print(
                    f"Patient: "
                    f"{appointment['patient_first_name']} "
                    f"{appointment['patient_last_name']}"
                )
                print(
                    f"Doctor: "
                    f"{appointment['doctor_first_name']} "
                    f"{appointment['doctor_last_name']}"
                )
                print(
                    f"Date: "
                    f"{appointment['appointment_date']}"
                )
                print(
                    f"Time: "
                    f"{appointment['appointment_time']}"
                )
                print(
                    f"Reason: "
                    f"{appointment['reason'] or ''}"
                )
                print(
                    f"Status: "
                    f"{appointment['status']}"
                )
                print("-" * 40)

        elif choice == "3":
            print("\n--- Search Appointment ---")

            try:
                appointment_id = int(
                    input("Enter appointment ID: ").strip()
                )
            except ValueError:
                print(
                    "\nPlease enter a valid numeric appointment ID."
                )
                continue

            appointment = appointment_service.get_appointment(
                appointment_id
            )

            if appointment:
                print("\nAppointment found:")
                print(
                    f"Appointment ID: "
                    f"{appointment['appointment_id']}"
                )
                print(
                    f"Patient: "
                    f"{appointment['patient_first_name']} "
                    f"{appointment['patient_last_name']}"
                )
                print(
                    f"Doctor: "
                    f"{appointment['doctor_first_name']} "
                    f"{appointment['doctor_last_name']}"
                )
                print(
                    f"Date: "
                    f"{appointment['appointment_date']}"
                )
                print(
                    f"Time: "
                    f"{appointment['appointment_time']}"
                )
                print(
                    f"Reason: "
                    f"{appointment['reason'] or ''}"
                )
                print(
                    f"Status: "
                    f"{appointment['status']}"
                )
            else:
                print("\nAppointment not found.")

        elif choice == "4":
            print("\n--- Update Appointment Status ---")

            try:
                appointment_id = int(
                    input("Appointment ID: ").strip()
                )
            except ValueError:
                print(
                    "\nPlease enter a valid numeric appointment ID."
                )
                continue

            print("\nAvailable statuses:")
            print("1. Scheduled")
            print("2. Completed")
            print("3. Cancelled")

            status_choice = input(
                "Choose status: "
            ).strip()

            status_map = {
                "1": "Scheduled",
                "2": "Completed",
                "3": "Cancelled"
            }

            if status_choice not in status_map:
                print("\nInvalid status.")
                continue

            status = status_map[status_choice]

            if appointment_service.update_status(
                appointment_id,
                status
            ):
                print(
                    "\nAppointment status updated successfully."
                )
            else:
                print(
                    "\nAppointment not found or update failed."
                )

        elif choice == "5":
            print("\n--- Delete Appointment ---")

            try:
                appointment_id = int(
                    input("Enter appointment ID: ").strip()
                )
            except ValueError:
                print(
                    "\nPlease enter a valid numeric appointment ID."
                )
                continue

            appointment = appointment_service.get_appointment(
                appointment_id
            )

            if not appointment:
                print("\nAppointment not found.")
                continue

            confirmation = input(
                "Are you sure you want to delete this appointment? (y/n): "
            ).strip().lower()

            if confirmation == "y":
                if appointment_service.delete_appointment(
                    appointment_id
                ):
                    print(
                        "\nAppointment deleted successfully."
                    )
                else:
                    print(
                        "\nFailed to delete appointment."
                    )
            else:
                print("\nDelete cancelled.")

        elif choice == "6":
            break

        else:
            print("\nInvalid choice. Please enter 1-6.")


# ============================================================
# MEDICAL RECORD MANAGEMENT
# ============================================================

def medical_record_menu():
    medical_record_service = MedicalRecordService()

    while True:
        print("\n" + "=" * 50)
        print("          MEDICAL RECORD MANAGEMENT")
        print("=" * 50)
        print("1. Add Medical Record")
        print("2. View All Medical Records")
        print("3. Search Medical Record")
        print("4. Delete Medical Record")
        print("5. Back to Main Menu")
        print("=" * 50)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            print("\n--- Add New Medical Record ---")

            try:
                patient_id = int(
                    input("Patient ID: ").strip()
                )
                doctor_id = int(
                    input("Doctor ID: ").strip()
                )
            except ValueError:
                print(
                    "\nPatient ID and Doctor ID must be numbers."
                )
                continue

            appointment_input = input(
                "Appointment ID (press Enter if none): "
            ).strip()

            if appointment_input:
                try:
                    appointment_id = int(appointment_input)
                except ValueError:
                    print(
                        "\nAppointment ID must be a number."
                    )
                    continue
            else:
                appointment_id = None

            diagnosis = input(
                "Diagnosis: "
            ).strip()

            treatment = input(
                "Treatment: "
            ).strip()

            notes = input(
                "Notes: "
            ).strip()

            record = medical_record_service.add_medical_record(
                patient_id=patient_id,
                doctor_id=doctor_id,
                appointment_id=appointment_id,
                diagnosis=diagnosis,
                treatment=treatment,
                notes=notes
            )

            if record:
                print("\nMedical record added successfully!")
                print(record)
            else:
                print("\nFailed to add medical record.")

        elif choice == "2":
            print("\n--- All Medical Records ---")

            records = (
                medical_record_service.get_all_medical_records()
            )

            if not records:
                print("No medical records found.")
                continue

            for record in records:
                print(
                    f"\nRecord ID: "
                    f"{record['record_id']}"
                )
                print(
                    f"Patient: "
                    f"{record['patient_first_name']} "
                    f"{record['patient_last_name']}"
                )
                print(
                    f"Doctor: "
                    f"{record['doctor_first_name']} "
                    f"{record['doctor_last_name']}"
                )
                print(
                    f"Appointment ID: "
                    f"{record['appointment_id']}"
                )
                print(
                    f"Diagnosis: "
                    f"{record['diagnosis']}"
                )
                print(
                    f"Treatment: "
                    f"{record['treatment']}"
                )
                print(
                    f"Notes: "
                    f"{record['notes']}"
                )
                print(
                    f"Created At: "
                    f"{record['created_at']}"
                )
                print("-" * 40)

        elif choice == "3":
            print("\n--- Search Medical Record ---")

            try:
                record_id = int(
                    input("Enter record ID: ").strip()
                )
            except ValueError:
                print(
                    "\nPlease enter a valid numeric record ID."
                )
                continue

            record = medical_record_service.get_medical_record(
                record_id
            )

            if record:
                print("\nMedical record found:")
                print(
                    f"Record ID: "
                    f"{record['record_id']}"
                )
                print(
                    f"Patient: "
                    f"{record['patient_first_name']} "
                    f"{record['patient_last_name']}"
                )
                print(
                    f"Doctor: "
                    f"{record['doctor_first_name']} "
                    f"{record['doctor_last_name']}"
                )
                print(
                    f"Appointment ID: "
                    f"{record['appointment_id']}"
                )
                print(
                    f"Diagnosis: "
                    f"{record['diagnosis']}"
                )
                print(
                    f"Treatment: "
                    f"{record['treatment']}"
                )
                print(
                    f"Notes: "
                    f"{record['notes']}"
                )
                print(
                    f"Created At: "
                    f"{record['created_at']}"
                )
            else:
                print("\nMedical record not found.")

        elif choice == "4":
            print("\n--- Delete Medical Record ---")

            try:
                record_id = int(
                    input("Enter record ID: ").strip()
                )
            except ValueError:
                print(
                    "\nPlease enter a valid numeric record ID."
                )
                continue

            record = medical_record_service.get_medical_record(
                record_id
            )

            if not record:
                print("\nMedical record not found.")
                continue

            confirmation = input(
                "Are you sure you want to delete this medical record? (y/n): "
            ).strip().lower()

            if confirmation == "y":
                if medical_record_service.delete_medical_record(
                    record_id
                ):
                    print(
                        "\nMedical record deleted successfully."
                    )
                else:
                    print(
                        "\nFailed to delete medical record."
                    )
            else:
                print("\nDelete cancelled.")

        elif choice == "5":
            break

        else:
            print("\nInvalid choice. Please enter 1-5.")


# ============================================================
# BILLING MANAGEMENT
# ============================================================

def billing_menu():
    billing_service = BillingService()

    while True:
        print("\n" + "=" * 50)
        print("             BILLING MANAGEMENT")
        print("=" * 50)
        print("1. Add Bill")
        print("2. View All Bills")
        print("3. Search Bill")
        print("4. Update Bill Status")
        print("5. Delete Bill")
        print("6. Back to Main Menu")
        print("=" * 50)

        choice = input("Enter your choice: ").strip()

        # ----------------------------------------------------
        # ADD BILL
        # ----------------------------------------------------

        if choice == "1":
            print("\n--- Add New Bill ---")

            try:
                patient_id = int(
                    input("Patient ID: ").strip()
                )
            except ValueError:
                print("\nPatient ID must be a number.")
                continue

            appointment_input = input(
                "Appointment ID (press Enter if none): "
            ).strip()

            if appointment_input:
                try:
                    appointment_id = int(
                        appointment_input
                    )
                except ValueError:
                    print(
                        "\nAppointment ID must be a number."
                    )
                    continue
            else:
                appointment_id = None

            try:
                amount = float(
                    input("Amount: ").strip()
                )
            except ValueError:
                print(
                    "\nAmount must be a valid number."
                )
                continue

            if amount < 0:
                print("\nAmount cannot be negative.")
                continue

            description = input(
                "Description: "
            ).strip()

            print("\nPayment status:")
            print("1. Unpaid")
            print("2. Paid")
            print("3. Cancelled")

            status_choice = input(
                "Choose status: "
            ).strip()

            status_map = {
                "1": "Unpaid",
                "2": "Paid",
                "3": "Cancelled"
            }

            if status_choice not in status_map:
                print("\nInvalid status.")
                continue

            status = status_map[status_choice]

            bill = billing_service.add_bill(
                patient_id=patient_id,
                appointment_id=appointment_id,
                amount=amount,
                description=description,
                status=status
            )

            if bill:
                print("\nBill added successfully!")
                print(bill)
            else:
                print("\nFailed to add bill.")

        # ----------------------------------------------------
        # VIEW ALL BILLS
        # ----------------------------------------------------

        elif choice == "2":
            print("\n--- All Bills ---")

            bills = billing_service.get_all_bills()

            if not bills:
                print("No bills found.")
                continue

            for bill in bills:
                print(
                    f"\nBill ID: "
                    f"{bill['bill_id']}"
                )

                print(
                    f"Patient: "
                    f"{bill['patient_first_name']} "
                    f"{bill['patient_last_name']}"
                )

                print(
                    f"Appointment ID: "
                    f"{bill['appointment_id']}"
                )

                print(
                    f"Amount: "
                    f"K{float(bill['amount']):.2f}"
                )

                print(
                    f"Description: "
                    f"{bill['description'] or ''}"
                )

                print(
                    f"Status: "
                    f"{bill['status']}"
                )

                print(
                    f"Payment Date: "
                    f"{bill['payment_date'] or 'Not paid'}"
                )

                print(
                    f"Created At: "
                    f"{bill['created_at']}"
                )

                print("-" * 40)

        # ----------------------------------------------------
        # SEARCH BILL
        # ----------------------------------------------------

        elif choice == "3":
            print("\n--- Search Bill ---")

            try:
                bill_id = int(
                    input("Enter bill ID: ").strip()
                )
            except ValueError:
                print(
                    "\nPlease enter a valid numeric bill ID."
                )
                continue

            bill = billing_service.get_bill(bill_id)

            if bill:
                print("\nBill found:")

                print(
                    f"Bill ID: "
                    f"{bill['bill_id']}"
                )

                print(
                    f"Patient: "
                    f"{bill['patient_first_name']} "
                    f"{bill['patient_last_name']}"
                )

                print(
                    f"Appointment ID: "
                    f"{bill['appointment_id']}"
                )

                print(
                    f"Amount: "
                    f"K{float(bill['amount']):.2f}"
                )

                print(
                    f"Description: "
                    f"{bill['description'] or ''}"
                )

                print(
                    f"Status: "
                    f"{bill['status']}"
                )

                print(
                    f"Payment Date: "
                    f"{bill['payment_date'] or 'Not paid'}"
                )

                print(
                    f"Created At: "
                    f"{bill['created_at']}"
                )

            else:
                print("\nBill not found.")

        # ----------------------------------------------------
        # UPDATE BILL STATUS
        # ----------------------------------------------------

        elif choice == "4":
            print("\n--- Update Bill Status ---")

            try:
                bill_id = int(
                    input("Bill ID: ").strip()
                )
            except ValueError:
                print(
                    "\nPlease enter a valid numeric bill ID."
                )
                continue

            print("\nAvailable statuses:")
            print("1. Paid")
            print("2. Unpaid")
            print("3. Cancelled")

            status_choice = input(
                "Choose status: "
            ).strip()

            status_map = {
                "1": "Paid",
                "2": "Unpaid",
                "3": "Cancelled"
            }

            if status_choice not in status_map:
                print("\nInvalid status.")
                continue

            status = status_map[status_choice]

            if billing_service.update_bill_status(
                bill_id,
                status
            ):
                print(
                    "\nBill status updated successfully."
                )
            else:
                print(
                    "\nBill not found or update failed."
                )

        # ----------------------------------------------------
        # DELETE BILL
        # ----------------------------------------------------

        elif choice == "5":
            print("\n--- Delete Bill ---")

            try:
                bill_id = int(
                    input("Enter bill ID: ").strip()
                )
            except ValueError:
                print(
                    "\nPlease enter a valid numeric bill ID."
                )
                continue

            bill = billing_service.get_bill(bill_id)

            if not bill:
                print("\nBill not found.")
                continue

            print(
                f"\nBill ID: {bill['bill_id']}"
            )
            print(
                f"Amount: K{float(bill['amount']):.2f}"
            )
            print(
                f"Status: {bill['status']}"
            )

            confirmation = input(
                "Are you sure you want to delete this bill? (y/n): "
            ).strip().lower()

            if confirmation == "y":
                if billing_service.delete_bill(bill_id):
                    print("\nBill deleted successfully.")
                else:
                    print("\nFailed to delete bill.")
            else:
                print("\nDelete cancelled.")

        # ----------------------------------------------------
        # BACK TO MAIN MENU
        # ----------------------------------------------------

        elif choice == "6":
            break

        else:
            print("\nInvalid choice. Please enter 1-6.")


# ============================================================
# ADMINISTRATOR MANAGEMENT
# ============================================================

def administrator_menu():
    administrator_service = AdministratorService()

    while True:
        print("\n" + "=" * 50)
        print("          ADMINISTRATOR MANAGEMENT")
        print("=" * 50)
        print("1. Add Administrator")
        print("2. View All Administrators")
        print("3. Search Administrator")
        print("4. Delete Administrator")
        print("5. Back to Main Menu")
        print("=" * 50)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            print("\n--- Add New Administrator ---")

            full_name = input(
                "Full name: "
            ).strip()

            email = input(
                "Email: "
            ).strip()

            phone = input(
                "Phone: "
            ).strip()

            if not full_name:
                print("\nFull name is required.")
                continue

            administrator = (
                administrator_service.add_administrator(
                    full_name=full_name,
                    email=email,
                    phone=phone
                )
            )

            if administrator:
                print(
                    "\nAdministrator added successfully!"
                )
                print(
                    f"Administrator ID: "
                    f"{administrator['admin_id']}"
                )
                print(
                    f"Name: "
                    f"{administrator['full_name']}"
                )
                print(
                    f"Email: "
                    f"{administrator['email']}"
                )
                print(
                    f"Phone: "
                    f"{administrator['phone']}"
                )
            else:
                print(
                    "\nFailed to add administrator."
                )

        elif choice == "2":
            print("\n--- All Administrators ---")

            administrators = (
                administrator_service
                .get_all_administrators()
            )

            if not administrators:
                print("No administrators found.")
                continue

            for administrator in administrators:
                print(
                    f"\nAdministrator ID: "
                    f"{administrator['admin_id']}"
                )
                print(
                    f"User ID: "
                    f"{administrator['user_id']}"
                )
                print(
                    f"Name: "
                    f"{administrator['full_name']}"
                )
                print(
                    f"Email: "
                    f"{administrator['email']}"
                )
                print(
                    f"Phone: "
                    f"{administrator['phone']}"
                )
                print("-" * 40)

        elif choice == "3":
            print("\n--- Search Administrator ---")

            try:
                admin_id = int(
                    input(
                        "Enter administrator ID: "
                    ).strip()
                )
            except ValueError:
                print(
                    "\nPlease enter a valid numeric administrator ID."
                )
                continue

            administrator = (
                administrator_service
                .get_administrator(admin_id)
            )

            if administrator:
                print("\nAdministrator found:")
                print(
                    f"Administrator ID: "
                    f"{administrator['admin_id']}"
                )
                print(
                    f"User ID: "
                    f"{administrator['user_id']}"
                )
                print(
                    f"Name: "
                    f"{administrator['full_name']}"
                )
                print(
                    f"Email: "
                    f"{administrator['email']}"
                )
                print(
                    f"Phone: "
                    f"{administrator['phone']}"
                )
            else:
                print(
                    "\nAdministrator not found."
                )

        elif choice == "4":
            print("\n--- Delete Administrator ---")

            try:
                admin_id = int(
                    input(
                        "Enter administrator ID: "
                    ).strip()
                )
            except ValueError:
                print(
                    "\nPlease enter a valid numeric administrator ID."
                )
                continue

            administrator = (
                administrator_service
                .get_administrator(admin_id)
            )

            if not administrator:
                print(
                    "\nAdministrator not found."
                )
                continue

            print(
                f"\nAdministrator: "
                f"{administrator['full_name']}"
            )

            confirmation = input(
                "Are you sure you want to delete this administrator? (y/n): "
            ).strip().lower()

            if confirmation == "y":
                if administrator_service.delete_administrator(
                    admin_id
                ):
                    print(
                        "\nAdministrator deleted successfully."
                    )
                else:
                    print(
                        "\nFailed to delete administrator."
                    )
            else:
                print("\nDelete cancelled.")

        elif choice == "5":
            break

        else:
            print("\nInvalid choice. Please enter 1-5.")


# ============================================================
# MAIN MENU
# ============================================================

def show_main_menu():
    print("\n" + "=" * 50)
    print("       HOSPITAL MANAGEMENT SYSTEM")
    print("=" * 50)
    print("1. Patient Management")
    print("2. Doctor Management")
    print("3. Appointment Management")
    print("4. Medical Records")
    print("5. Billing")
    print("6. Administrator")
    print("7. Exit")
    print("=" * 50)


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():
    print("\nHospital Management System is starting...")

    database_manager = DatabaseManager()

    if not database_manager.test_connection():
        print("\nUnable to connect to the MySQL database.")
        print(
            "Please check your MySQL/XAMPP server "
            "and database settings."
        )
        return

    while True:
        show_main_menu()

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":
            patient_menu()

        elif choice == "2":
            doctor_menu()

        elif choice == "3":
            appointment_menu()

        elif choice == "4":
            medical_record_menu()

        elif choice == "5":
            billing_menu()

        elif choice == "6":
            administrator_menu()

        elif choice == "7":
            print(
                "\nThank you for using the "
                "Hospital Management System."
            )
            break

        else:
            print(
                "\nInvalid choice. "
                "Please enter a number from 1 to 7."
            )


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":
    main()