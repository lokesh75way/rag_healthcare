from typing import Any, Dict

import requests

from config.settings import settings


class HealthcareService:
    
    def __init__(self):
        self.base_url = settings.backend_api_url
        self.api_key = settings.backend_api_key
    
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _call_api(self, endpoint: str, method: str = "GET", payload: Dict[str, Any] = None) -> Any:
        """Helper to call external service"""
        url = f"{self.base_url}/{endpoint}"
        try:
            if method == "GET":
                response = requests.get(url, headers=self.headers, params=payload, timeout=10)
            else:  # POST
                response = requests.post(url, headers=self.headers, json=payload, timeout=10)

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return str(e)

    # ---------------- TOOLS ---------------- #
    def get_doctors(self, specialty: str = "", name: str = "") -> Any:
        """Fetch doctors by specialty or name"""
        payload = {"specialty": specialty, "name": name}
        return self._call_api("/doctors", "GET", payload)

    def get_slots(self, doctor_id: str) -> Any:
        """Fetch available slots for a doctor"""
        payload = {"doctor_id": doctor_id}
        return self._call_api("/slots", "GET", payload)

    def book(self, doctor_id: str, user_id: str, time: str) -> Any:
        """Book an appointment"""
        payload = {"doctor_id": doctor_id, "user_id": user_id, "time": time}
        return self._call_api("/book", "POST", payload)

    def cancel(self, doctor_id: str, user_id: str, time: str) -> Any:
        """Cancel an appointment"""
        payload = {"doctor_id": doctor_id, "user_id": user_id, "time": time}
        return self._call_api("/cancel", "POST", payload)

    def reschedule(self, doctor_id: str, user_id: str, old_time: str, new_time: str) -> Any:
        """Reschedule an appointment"""
        payload = {
            "doctor_id": doctor_id,
            "user_id": user_id,
            "old_time": old_time,
            "new_time": new_time
        }
        return self._call_api("/reschedule", "POST", payload)
