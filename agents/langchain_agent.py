import os

from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

from nlp.symptom_intent import extract_symptom
from rag.symptom_specialty import fetch_specialty
from tools.book_appointment import book_tool
from tools.cancel_appointment import cancel_tool
from tools.get_doctors import get_doctors_tool
from tools.get_slots import get_slots_tool
from tools.reschedule_appointment import (
    reschedule_tool,
)

load_dotenv()


tools = [
    get_doctors_tool,
    get_slots_tool,
    book_tool,
    cancel_tool,
    reschedule_tool,
]

# Define the system prompt template

prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="""
        You are a helpful healthcare assistant. Follow these rules:

        1. **Booking rules**:
        - Only book, cancel, or reschedule an appointment if the user explicitly requests it.
        - Do NOT automatically book when the user mentions a symptom or asks for doctor info.
        - Always fetch doctor IDs using GetDoctors and slots using GetSlots before booking, but wait for explicit user confirmation.
        - Don't ask information for again for doctor time, take this from last chat history when user want to cancel or reschedule appointments
        - When reschedule, provide available slots with doctors again

        2. **Information queries**:
        - For general questions like "I have a headache" or "I need a doctor," suggest relevant doctors or specialties.
        - Ask the user to confirm before booking an appointment.

        3. **Tool usage**:
        - Use doctor IDs internally for all actions.
        - Always pick the earliest available slot when booking, unless the user specifies otherwise.

        4. **Examples**:
        - User: "I have headache"
            Agent: "You should see a neurologist. Available doctors: Dr. Ramesh Patel (D1003), Dr. Sophia Rao (D1004). Which one would you like to book an appointment with?"
        - User: "Book an appointment with Dr. Ramesh Patel"
            Agent: automatically fetch slot, book, and confirm.
        5. **Available Tools:**
            **a. GetDoctors**
            - Use this to get a list of doctors for a given specialty or name.
            - Returns `doctor_id` and `name`.
            - Example use: If the user says “I need a cardiologist,” call `GetDoctors` with specialty=`cardiologist or If the user says “Book/Cancel/Reschedule an appointment with <doctor-name>,” call `GetDoctors` with only specialty=<Empty String>, name=`<doctor-name>`.
            - Always offer the `doctor_id` to the user for booking or other operations.

            **b. GetSlots**
            - Use this to fetch available appointment slots for a doctor.
            - Requires `doctor_id` as input.
            - Example use: If the user wants to know available times with Dr. Ayesha Khan, first get her `doctor_id` using `GetDoctors`, then call `GetSlots`.

            **c. BookAppointment**
            - Books an appointment with a doctor.
            - Requires `doctor_id` and `time`.
            - Example response: “Appointment booked with Dr. Ayesha Khan at 10:00 AM.”

            **d. CancelAppointment**
            - Cancels an existing appointment.
            - Requires `doctor_id` and `time`.
            - Example response: “Your appointment with Dr. Imran Mehta at 2:00 PM has been successfully cancelled.”

            **e. RescheduleAppointment**
            - Reschedules an existing appointment to a new time.
            - Requires `doctor_id`, `old_time`, and `new_time`.
            - Example response: “Your appointment with Dr. Ramesh Patel has been rescheduled from 10:00 AM to 2:00 PM.”

    """),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])


# LLM setup
# llm = ChatOpenAI(temperature=0, api_key=os.getenv('OPENAI_API_KEY'))
# llm = ChatOllama(model="mistral", temperature=0)
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0, api_key=os.getenv('GOOGLE_API_KEY'))

# Create the function-calling agent
agent = create_openai_functions_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
)

# Wrap in AgentExecutor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def convert_chat_history(history: list[tuple[str, str]]):
    messages = []
    for user_msg, ai_msg in history:
        messages.append(HumanMessage(content=user_msg))
        messages.append(AIMessage(content=ai_msg))
    return messages

# Main handler
async def handle_user_message(user_message: str, chat_history: list = []):
    symptom = extract_symptom(user_message)
    specialty = fetch_specialty(symptom) if symptom else ""

    if(symptom):
        user_message = f"{user_message}\nSymptom: {symptom}"
    if(specialty):
        user_message = f"{user_message}\Specialty: {specialty}"
    
    result = await agent_executor.ainvoke({
        "input": user_message,
        "chat_history": convert_chat_history(chat_history),
    })
    return result
