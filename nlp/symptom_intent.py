SYMPTOMS = [
    "chest pain", "headache", "fever", "cough", "back pain", "sore throat",
    "fatigue", "dizziness", "nausea", "shortness of breath"
]


def extract_symptom(user_message: str):
    found_symptom = None
    for symptom in SYMPTOMS:
        if symptom in user_message.lower():
            found_symptom = symptom
            break
    return found_symptom
