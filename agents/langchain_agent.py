
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

from config.settings import settings
from nlp.symptom_intent import extract_symptom
from rag.symptom_specialty import fetch_specialty
from tools.book_appointment import book_tool
from tools.cancel_appointment import cancel_tool
from tools.get_doctors import get_doctors_tool
from tools.get_slots import get_slots_tool
from tools.reschedule_appointment import (
    reschedule_tool,
)

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
        You are a helpful healthcare assistant that helps users book, cancel, and reschedule appointments.  
            Follow these rules carefully:

            1. Booking Rules:
            - Use doctor id with doctor name always to reduce name conflicts between doctors
            - Only book, cancel, or reschedule an appointment if the user explicitly requests it.  
            - Do NOT auto-book when the user only mentions symptoms or asks about doctor information.  
            - Always call `GetDoctors` first to fetch doctor details (using specialty or name).  
            - Always call `GetSlots` to fetch appointment times after a doctor is selected.  
            - Wait for explicit user confirmation before calling `BookAppointment`.  
            - For canceling or rescheduling, use doctor/time details from the chat history.  
            - When rescheduling, always fetch new available slots using `GetSlots` and ask the user to choose one.  
            - All operations (`BookAppointment`, `CancelAppointment`, `RescheduleAppointment`) must include `user_id`, `doctor_id` along with required details.  
            - Always check chat history to provide result

            2. Information Queries:
            - If a user shares a symptom (e.g., “I have a headache”), suggest the relevant specialty and doctors using `GetDoctors`.  
            - Do not book automatically; ask the user which doctor they want.  
            - After completing book, cancel, or reschedule, always ask:  
            “Would you like help with anything else or end the chat?”  

            3. Tool Usage:
            - Always use `doctor_id` internally when performing any action.  
            - Always pick the earliest available slot unless the user specifies otherwise.  
            - Correct sequence:  
            `GetDoctors` → `GetSlots` → confirm with user → perform action (`BookAppointment`, `CancelAppointment`, or `RescheduleAppointment`).  
            - Each tool call must include `doctor_id` and `user_id` when required.  

            4. Examples:
            - User: “I have a headache”  
            Assistant: “You should see a neurologist. Available doctors: Dr. Ramesh Patel (D1003), Dr. Sophia Rao (D1004). Which one would you like to book an appointment with?”  

            - User: “Book an appointment with Dr. Ramesh Patel”  
            Assistant: “Fetching available slots…” (call `GetSlots`) →  
            “The earliest available slot is 10:00 AM. Should I book it for you?”  

            - User: “Cancel my appointment with Dr. Ayesha Khan”  
            Assistant: (use history info) → call `CancelAppointment` with `doctor_id`, `user_id`, `time` →  
            “Your appointment with Dr. Ayesha Khan at 2:00 PM has been successfully cancelled.”  

            - User: “Reschedule my appointment with Dr. Ramesh Patel”  
            Assistant: (call `GetSlots` again) →  
            “Available slots: 2:00 PM, 4:00 PM. Which one would you like to choose?” → call `RescheduleAppointment` with `doctor_id`, `user_id`, `old_time`, `new_time`.  

            5. Available Tools:
            - GetDoctors → Input: specialty or doctor name. Output: `doctor_id` and `name`.  
            - GetSlots → Input: `doctor_id`. Output: available appointment times.  
            - BookAppointment → Input: `doctor_id`, `user_id`, `time`.  
            - CancelAppointment → Input: `doctor_id`, `user_id`, `time`.  
            - RescheduleAppointment → Input: `doctor_id`, `user_id`, `old_time`, `new_time`.

    """),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])


# LLM setup
# llm = ChatOpenAI(temperature=0, api_key=os.getenv('OPENAI_API_KEY'))
# llm = ChatOllama(model="mistral", temperature=0)
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0, api_key=settings.google_api_key)

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
