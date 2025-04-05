# agents/routing_agent.py

import requests
import random
from config import API_KEY


class RoutingAgent:
    def __init__(self):
        pass

    def get_traffic_data(self, lat, lon):
        url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/relative0/10/json"
        params = {"point": f"{lat},{lon}", "unit": "KMPH", "key": API_KEY}
        try:
            res = requests.get(url, params=params)
            return res.json().get("flowSegmentData", {})
        except Exception as e:
            print("Exception in get_traffic_data:", e)
            return {"currentSpeed": random.randint(10, 60), "freeFlowSpeed": 60}

    def route_vehicle(self, vehicle, traffic_data):
        if traffic_data.get("currentSpeed", 0) < 20:
            return f"{vehicle['id']} → rerouted to avoid congestion."
        return f"{vehicle['id']} → continue on current path."
