from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

from services.backend import HealthcareService

healthcare_service = HealthcareService()

# Schema for input args
class GetSlotsArgs(BaseModel):
    doctor_id: str = Field(..., description="Unique ID of the doctor to fetch slots for")


# Function stays simple
def get_slots(doctor_id: str) -> list[str]:
    """
    Retrieve a list of available appointment slots for the given doctor id.
    """

    return healthcare_service.get_slots(doctor_id=doctor_id)


# Register tool
get_slots_tool = StructuredTool.from_function(
    func=get_slots,
    name="GetSlots",
    description="Fetch available appointment slots for a doctor using doctor_id.",
    args_schema=GetSlotsArgs,
)
