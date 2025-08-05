import os
from dotenv import load_dotenv
from tools.get_doctors import get_doctors
from tools.get_slots import get_slots
from tools.book_appointment import book_appointment
from tools.cancel_appointment import cancel_appointment
from tools.reschedule_appointment import reschedule_appointment
from nlp.symptom_intent import extract_symptom
from rag.symptom_specialty import fetch_specialty

from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_functions_agent, AgentExecutor, Tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

# Load tools decorated with @tool
# tools = [
#     get_doctors,
#     get_slots,
#     book_appointment,
#     cancel_appointment,
#     reschedule_appointment,
# ]

tools = [
    Tool(name="GetDoctors", func=get_doctors, description="Get list of doctors for a specialty"),
    Tool(name="GetSlots", func=get_slots, description="Fetch available appointment slots for doctor"),
    Tool(name="BookAppointment", func=book_appointment, description="Book an appointment with provided time and doctor"),
    Tool(name="CancelAppointment", func=cancel_appointment, description="Cancel an appointment with doctor on provided time"),
    Tool(name="RescheduleAppointment", func=reschedule_appointment, description="Reschedule an appointment from old to new time"),
]

# Define the system prompt template
prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="You are a healthcare assistant. Use tools to answer user queries."),
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
async def handle_user_message(user_message: str, chat_history: list = []) -> str:
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
