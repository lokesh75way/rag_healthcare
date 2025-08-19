from langchain.tools import StructuredTool
from pydantic import BaseModel, Field


# Schema for input args
class GetSlotsArgs(BaseModel):
    doctor_id: str = Field(..., description="Unique ID of the doctor to fetch slots for")


# Function stays simple
def get_slots(doctor_id: str) -> list[str]:
    """
    Retrieve a list of available appointment slots for the given doctor id.
    """
    print(f"Fetching slots for doctor {doctor_id}")
    return ["10:00 AM", "2:00 PM", "4:30 PM"]


# Register tool
get_slots_tool = StructuredTool.from_function(
    func=get_slots,
    name="GetSlots",
    description="Fetch available appointment slots for a doctor using doctor_id.",
    args_schema=GetSlotsArgs,
)
