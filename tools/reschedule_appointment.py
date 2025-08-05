from langchain_core.tools import tool


@tool
def reschedule_appointment(old_time: str, new_time: str) -> str:
    """
    Reschedule an existing appointment to a different time slot with provided time.
    """
    
    return "🔁 Your appointment has been rescheduled to the next available slot."
