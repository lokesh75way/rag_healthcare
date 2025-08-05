from langchain_core.tools import tool


@tool
def book_appointment(time: str, doctor: str = None) -> str:
    """
    Book an appointment with a doctor based on provide time and doctor id.
    """

    return (
        f"✅ Appointment booked with {doctor} at {time}"
    )
