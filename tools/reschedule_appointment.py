from langchain.tools import StructuredTool
from pydantic import BaseModel, Field


# Schema for input arguments
class RescheduleArgs(BaseModel):
    doctor_id: str = Field(..., description="Unique ID of the doctor")
    old_time: str = Field(..., description="Original appointment time")
    new_time: str = Field(..., description="New appointment time to reschedule to")

# Function stays simple
def reschedule_appointment(doctor_id: str, old_time: str, new_time: str) -> str:
    """Reschedule an appointment with the doctor by ID from old_time to new_time"""
    print(doctor_id, old_time, new_time)
    return "🔁 Your appointment has been rescheduled to the new time."

# Register tool properly
reschedule_tool = StructuredTool.from_function(
    func=reschedule_appointment,
    name="RescheduleAppointment",
    description="Reschedule an existing appointment by providing doctor_id, old_time, and new_time",
    args_schema=RescheduleArgs,
)
