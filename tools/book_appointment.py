from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

from services.backend import HealthcareService

healthcare_service = HealthcareService()

# Define the schema
class BookArgs(BaseModel):
    doctor_id: str = Field(..., description="Unique ID of the doctor")
    user_id: str = Field(..., description="Unique User id of the doctor")
    time: str = Field(..., description="Appointment time in human-readable format")



# Function stays simple
def book_appointment(doctor_id: str, user_id: str, time: str) -> str:
    """
    Book an appointment with a doctor based on provided doctor id, user id and time.
    """
    return healthcare_service.book(doctor_id=doctor_id, user_id=user_id, time=time)


# Register as StructuredTool
book_tool = StructuredTool.from_function(
    func=book_appointment,
    name="BookAppointment",
    description="Book an appointment by providing doctor_id, user_id and time.",
    args_schema=BookArgs,
)
