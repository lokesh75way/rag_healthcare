
from langchain_core.tools import tool

# Mock doctors with IDs per specialty
DOCTOR_DIRECTORY = {
    "cardiologist": [
        {"id": "D1001", "name": "Dr. Ayesha Khan"},
        {"id": "D1002", "name": "Dr. Imran Mehta"}
    ],
    "neurologist": [
        {"id": "D1003", "name": "Dr. Ramesh Patel"},
        {"id": "D1004", "name": "Dr. Sophia Rao"}
    ],
    "general physician": [
        {"id": "D1005", "name": "Dr. Emily Chen"},
        {"id": "D1006", "name": "Dr. Raj Malhotra"}
    ],
    "pulmonologist": [
        {"id": "D1007", "name": "Dr. Anita Singh"},
        {"id": "D1008", "name": "Dr. Omar Farooq"}
    ],
    "orthopedic": [
        {"id": "D1009", "name": "Dr. Rahul Verma"},
        {"id": "D1010", "name": "Dr. Lisa Thomas"}
    ],
    "ENT specialist": [
        {"id": "D1011", "name": "Dr. Meera Sharma"},
        {"id": "D1012", "name": "Dr. Sanjay Kapoor"}
    ],
    "gastroenterologist": [
        {"id": "D1013", "name": "Dr. Neha Das"},
        {"id": "D1014", "name": "Dr. Vikram Iyer"}
    ]
}

@tool
def get_doctors(specialty: str = "general physician") -> str:
    """
     Retrieve doctor data in structured format.
    """

    doctors = DOCTOR_DIRECTORY.get(specialty, [])
    return doctors
