# agents/smart_vehicle_agent.py


class SmartVehicleAgent:
    def __init__(self):
        pass

    def communicate(self, vehicle):
        """
        Simulate smart vehicle communication based on its mode.
        """
        if vehicle.mode.lower() == "emergency":
            return f"{vehicle.id} is an EMERGENCY vehicle. Requesting immediate green light!"
        elif vehicle.mode.lower() == "autonomous":
            return f"{vehicle.id} (autonomous) reporting: All systems normal and environment monitored."
        elif vehicle.mode.lower() == "eco":
            return f"{vehicle.id} is in eco-mode. Optimizing fuel efficiency and reducing emissions."
        else:
            return f"{vehicle.id} reports normal status."

    def send_update(self, vehicle, update_message):
        """
        Simulate sending an update message to the vehicle.
        """
        print(f"[SmartVehicleAgent] Sending update to {vehicle.id}: {update_message}")
