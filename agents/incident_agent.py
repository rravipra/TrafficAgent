# agents/incident_agent.py


class IncidentAgent:
    def __init__(self):
        pass

    def detect_incident(self, traffic_data):
        return traffic_data.get("currentSpeed", 100) < 10
