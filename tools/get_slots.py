from langchain_core.tools import tool


@tool
def get_slots(doctor: str) -> str:
    """
    Retrieve a list of available appointment slots for the given doctor id.
    """
    
    return (
        f"⏰ Available slots"
        f"- 10:00 AM\n"
        f"- 2:00 PM\n"
        f"- 4:30 PM"
    )
