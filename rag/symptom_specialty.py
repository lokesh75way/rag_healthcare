def fetch_specialty(symptom: str) -> str:
    """
    Retrieve the medical specialty based on the symptom.
    """
    symptom = symptom.lower().strip() if symptom else ""

    symptom_to_specialty = {
        "headache": "neurologist",
        "skin rash": "dermatologist",
        "chest pain": "cardiologist",
        "fever": "general physician",
        "cough": "pulmonologist",
        "back pain": "orthopedic",
        "sore throat": "ENT specialist",
        "fatigue": "general physician",
        "dizziness": "neurologist",
        "nausea": "gastroenterologist",
        "shortness of breath": "pulmonologist",
        "abdominal pain": "gastroenterologist",
        "joint pain": "rheumatologist",
        "blurred vision": "ophthalmologist"
    }

    return symptom_to_specialty.get(symptom, "")
