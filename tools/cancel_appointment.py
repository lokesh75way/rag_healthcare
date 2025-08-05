from langchain_core.tools import tool


@tool
def cancel_appointment(time: str, doctor: str) -> str:
    """
    Cancel a previously scheduled appointment on provided time and doctor id.
    """

    return "❌ Your appointment has been successfully cancelled."
