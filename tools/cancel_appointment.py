from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

from services.backend import HealthcareService

healthcare_service = HealthcareService()

# Schema for arguments
class CancelArgs(BaseModel):
    doctor_id: str = Field(..., description="Unique ID of the doctor")
    user_id: str = Field(..., description="Unique User id of the doctor")
    time: str = Field(..., description="Appointment time to cancel")


# Function itself stays simple
def cancel_appointment(doctor_id: str, user_id: str, time: str) -> str:
    """
    Cancel a previously scheduled appointment at the provided doctor id, user id and time.
    """
    return healthcare_service.cancel(doctor_id, user_id, time)


# Register tool properly
cancel_tool = StructuredTool.from_function(
    func=cancel_appointment,
    name="CancelAppointment",
    description="Cancel an existing appointment by providing doctor_id, user_id and time.",
    args_schema=CancelArgs,
)
