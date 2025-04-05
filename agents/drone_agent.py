# agents/drone_agent.py

import random


class DroneAgent:
    def __init__(self):
        pass

    def scan_traffic(self, intersection):
        """
        Simulate an aerial scan:
          - Returns a congestion metric.
          - Randomly indicates if an emergency is detected.
          - Also provides the detected approach direction (one of "N", "S", "E", "W").
        """
        congestion_metric = random.uniform(0, 1)
        emergency_detected = random.choice([True, False, False])
        approach_direction = random.choice(["N", "S", "E", "W"])
        return {
            "congestion_metric": congestion_metric,
            "emergency_detected": emergency_detected,
            "approach_direction": approach_direction,
        }
