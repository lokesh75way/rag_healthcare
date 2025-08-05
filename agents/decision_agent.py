from tools.get_doctors import get_doctors
from tools.get_slots import get_slots
from tools.book_appointment import book_appointment
from tools.cancel_appointment import cancel_appointment
from tools.reschedule_appointment import reschedule_appointment

def route_tool(intent):
    if intent == "book":
        return book_appointment
    elif intent == "cancel":
        return cancel_appointment
    elif intent == "reschedule":
        return reschedule_appointment
    return None
