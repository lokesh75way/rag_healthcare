from langchain.tools import StructuredTool
from pydantic import BaseModel, Field


# Define the schema
class BookArgs(BaseModel):
    doctor_id: str = Field(..., description="Unique ID of the doctor")
    time: str = Field(..., description="Appointment time in human-readable format")


# Function stays simple
def book_appointment(doctor_id: str, time: str) -> str:
    """
    Book an appointment with a doctor based on provided time and doctor id.
    """
    print(time, doctor_id)
    return f"✅ Appointment booked with {doctor_id} at {time}"


# Register as StructuredTool
book_tool = StructuredTool.from_function(
    func=book_appointment,
    name="BookAppointment",
    description="Book an appointment by providing doctor_id and time.",
    args_schema=BookArgs,
)
