from typing import List

from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

from services.backend import HealthcareService

healthcare_service = HealthcareService()


class GetDoctorsArgs(BaseModel):
    specialty: str = Field(
        default="general physician",
        description="Specialty of doctor to search for, e.g., cardiologist, neurologist, etc."
    )
    name: str = Field(
        default="",
        description="Optional: Name of the doctor to search for"
    )


class Doctor(BaseModel):
    id: str
    name: str


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


def get_doctors(specialty: str = "", name: str = "") -> List[Doctor]:
    """
    Retrieve doctor data based on specialty and/or partial name (word match).
    - If both `specialty` and `name` are provided, return doctors in that specialty whose name contains the search word (case-insensitive).
    - If only `specialty` is provided, return all doctors in that specialty.
    - If only `name` is provided, search all specialties for doctors whose names contain the search word.
    """

    return healthcare_service.get_doctors(specialty=specialty, name=name)


get_doctors_tool = StructuredTool.from_function(
    func=get_doctors,
    name="GetDoctors",
    description="Retrieve doctor IDs and names by specialty or by name (name takes priority).",
    args_schema=GetDoctorsArgs,
)
