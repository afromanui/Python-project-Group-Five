from database.database_manager import DatabaseManager
from models.appointment import Appointment


db = DatabaseManager()

appointment = Appointment(
    patient_id=1,
    doctor_id=1,
    appointment_date="2026-09-10",
    appointment_time="10:00:00",
    reason="General check-up",
    status="Scheduled"
)

appointment_id = db.add_appointment(appointment)

if appointment_id:
    print()
    print("Appointment created successfully!")
    print(f"Appointment ID: {appointment_id}")
else:
    print()
    print("Failed to create appointment.")