from langchain.tools import StructuredTool
from pydantic import BaseModel, Field


# Schema for arguments
class CancelArgs(BaseModel):
    doctor_id: str = Field(..., description="Unique ID of the doctor")
    time: str = Field(..., description="Appointment time to cancel")


# Function itself stays simple
def cancel_appointment(doctor_id: str, time: str) -> str:
    """
    Cancel a previously scheduled appointment at the provided time with the given doctor id.
    """
    print(doctor_id, time)
    return "❌ Your appointment has been successfully cancelled."


# Register tool properly
cancel_tool = StructuredTool.from_function(
    func=cancel_appointment,
    name="CancelAppointment",
    description="Cancel an existing appointment by providing doctor_id and time.",
    args_schema=CancelArgs,
)
