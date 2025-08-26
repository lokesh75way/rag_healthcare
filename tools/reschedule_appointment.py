from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

from services.backend import HealthcareService

healthcare_service = HealthcareService()

# Schema for input arguments
class RescheduleArgs(BaseModel):
    doctor_id: str = Field(..., description="Unique ID of the doctor")
    user_id: str = Field(..., description="Unique User id of the doctor")
    old_time: str = Field(..., description="Original appointment time")
    new_time: str = Field(..., description="New appointment time to reschedule to")

# Function stays simple
def reschedule_appointment(doctor_id: str, user_id: str, old_time: str, new_time: str) -> str:
    """Reschedule an appointment with provided doctor id, user id, old_time and new_time"""
    return healthcare_service.reschedule(doctor_id=doctor_id, user_id=user_id, old_time=old_time, new_time=new_time)

# Register tool properly
reschedule_tool = StructuredTool.from_function(
    func=reschedule_appointment,
    name="RescheduleAppointment",
    description="Reschedule an existing appointment by providing doctor_id, user_id, old_time, and new_time",
    args_schema=RescheduleArgs,
)
