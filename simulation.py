# simulation.py

import time
import json
from agents.traffic_signal_agent import TrafficSignalAgent
from agents.routing_agent import RoutingAgent
from agents.incident_agent import IncidentAgent
from agents.fairness_agent import FairnessAgent
from agents.smart_vehicle_agent import SmartVehicleAgent
from agents.drone_agent import DroneAgent
from agents.vehicle import Vehicle

# ANSI escape sequences for colored terminal output
ANSI_RESET = "\033[0m"
ANSI_GREEN = "\033[92m"
ANSI_YELLOW = "\033[93m"
ANSI_RED = "\033[91m"
ANSI_BLUE = "\033[94m"
ANSI_CYAN = "\033[96m"
ANSI_MAGENTA = "\033[95m"


def color_text(text, color):
    return f"{color}{text}{ANSI_RESET}"


def generate_scenario(scenario_type):
    if scenario_type == "rush_hour":
        return {"1st_Street": 0.9, "2nd_Street": 0.8, "3rd_Street": 0.2}
    elif scenario_type == "accident":
        return {"1st_Street": 0.1, "2nd_Street": 0.95, "3rd_Street": 0.5}
    else:
        return {"1st_Street": 0.3, "2nd_Street": 0.4, "3rd_Street": 0.3}


# Define sample intersections with coordinates
INTERSECTIONS = {
    "1st_Street": (37.7749, -122.4194),
    "2nd_Street": (37.7750, -122.4180),
    "3rd_Street": (37.7755, -122.4170),
}

# Create sample vehicles as Vehicle objects.
vehicles = [
    Vehicle(
        "V1",
        (37.7749, -122.4194),
        "Downtown",
        smart_vehicle=True,
        mode="autonomous",
        intersection="1st_Street",
    ),
    Vehicle(
        "V2",
        (37.7755, -122.4180),
        "Airport",
        smart_vehicle=True,
        mode="emergency",
        intersection="2nd_Street",
    ),
    Vehicle(
        "V3",
        (37.7760, -122.4170),
        "Park",
        smart_vehicle=True,
        mode="eco",
        intersection="3rd_Street",
    ),
]


def simulation_loop(steps=5, scenario="rush_hour"):
    # Instantiate agents
    signal_agent = TrafficSignalAgent()  # AI_AGENT_1
    routing_agent = RoutingAgent()  # AI_AGENT_2
    incident_agent = IncidentAgent()  # AI_AGENT_3
    fairness_agent = FairnessAgent()  # AI_AGENT_4
    smart_vehicle_agent = SmartVehicleAgent()  # AI_AGENT_5
    drone_agent = DroneAgent()  # AI_AGENT_6

    traffic_conditions = generate_scenario(scenario)
    print(color_text(f"--- Starting Simulation: {scenario.upper()} ---", ANSI_CYAN))

    for step in range(1, steps + 1):
        print(color_text(f"\n=== Simulation Step {step} ===", ANSI_MAGENTA))

        # 1. Adjust signals at each intersection using TrafficSignalAgent.
        intersection_signal_states = {}
        for intersection, coords in INTERSECTIONS.items():
            lat, lon = coords
            signal_state = signal_agent.adjust_signals(lat, lon, current_time=step * 10)
            intersection_signal_states[intersection] = signal_state
            print(color_text(f"\nIntersection: {intersection}", ANSI_BLUE))
            # Display signal state for each direction with color-coded lights and emojis.
            for direction, state in signal_state.items():
                current = state["current_color"].upper()
                if current == "GREEN":
                    color = ANSI_GREEN
                    circle = "🟢"
                elif current == "YELLOW":
                    color = ANSI_YELLOW
                    circle = "🟡"
                elif current == "RED":
                    color = ANSI_RED
                    circle = "🔴"
                else:
                    color = ANSI_RESET
                    circle = ""
                print(
                    f"  {direction}: {color_text(current + ' ' + circle, color)}  (Time Remaining: {state['time_remaining']}s, Next: {state['next_color']})"
                )

            # DroneAgent scans the intersection.
            drone_data = drone_agent.scan_traffic(intersection)
            if drone_data["emergency_detected"]:
                print(
                    color_text(
                        f"  [DroneAgent] Emergency detected at {intersection}! Prioritizing emergency response.",
                        ANSI_RED,
                    )
                )
                traffic_conditions[intersection] = 1.0
            else:
                traffic_conditions[intersection] = generate_scenario(scenario)[
                    intersection
                ]

        # 2. Process smart vehicles.
        for vehicle in vehicles:
            vehicle_intersection = vehicle.intersection
            current_wait = fairness_agent.wait_times.get(vehicle_intersection, 0)

            smart_msg = smart_vehicle_agent.communicate(vehicle)
            print(color_text(f"\n[SmartVehicleAgent] {smart_msg}", ANSI_CYAN))
            print(
                f"  Vehicle {vehicle.id} at intersection {vehicle_intersection} current wait time: {current_wait}s"
            )

            # For non-emergency vehicles, if wait time is high, update status to eco-mode.
            if not vehicle.mode.lower() == "emergency" and current_wait > 50:
                smart_vehicle_agent.send_update(
                    vehicle,
                    f"High wait time ({current_wait}s) at {vehicle_intersection}. Switching to eco-mode for efficiency.",
                )
                vehicle.update_mode("eco")
            elif vehicle.mode.lower() == "emergency":
                # Get approach direction from DroneAgent.
                drone_data_vehicle = drone_agent.scan_traffic(vehicle_intersection)
                approach_direction = drone_data_vehicle.get("approach_direction", "N")
                smart_vehicle_agent.send_update(
                    vehicle,
                    f"Emergency override active. Your approach from {approach_direction} is prioritized with green light.",
                )
                # Build an emergency override signal state based on the approach direction.
                emergency_signal_state = {}
                for d in ["N", "S", "E", "W"]:
                    if d == approach_direction:
                        emergency_signal_state[d] = {
                            "current_color": "GREEN",
                            "time_remaining": 30,
                            "next_color": "YELLOW",
                            "movements": {
                                "left": "GREEN",
                                "straight": "GREEN",
                                "right": "GREEN",
                            },
                        }
                    else:
                        emergency_signal_state[d] = {
                            "current_color": "RED",
                            "time_remaining": 30,
                            "next_color": "GREEN",
                            "movements": {
                                "left": "RED",
                                "straight": "RED",
                                "right": "RED",
                            },
                        }
                intersection_signal_states[vehicle_intersection] = (
                    emergency_signal_state
                )
                print(
                    color_text(
                        f"  [EMERGENCY OVERRIDE] Intersection {vehicle_intersection} signals overridden: GREEN for {approach_direction}; RED for others.",
                        ANSI_RED,
                    )
                )
            else:
                smart_vehicle_agent.send_update(
                    vehicle, "No changes. Continue on current path."
                )

            # Vehicle routing decision via RoutingAgent.
            lat, lon = vehicle.location
            traffic_data = routing_agent.get_traffic_data(lat, lon)
            route_msg = routing_agent.route_vehicle(vehicle, traffic_data)
            print(f"  [RoutingAgent] {route_msg}")

            # Incident detection via IncidentAgent.
            if incident_agent.detect_incident(traffic_data):
                print(
                    color_text(
                        f"  [IncidentAgent] Incident detected near vehicle {vehicle.id}!",
                        ANSI_RED,
                    )
                )
                traffic_conditions[vehicle_intersection] = max(
                    traffic_conditions.get(vehicle_intersection, 0), 0.9
                )

        # 3. Fairness updates: update wait times based on current congestion.
        for intersection, congestion in traffic_conditions.items():
            fairness_agent.update_fairness(intersection, congestion * 10)
        fairness_plan = fairness_agent.get_fair_signal_plan()
        print(
            color_text(
                "\n[FairnessAgent] Fairness-based priority (highest wait times):",
                ANSI_YELLOW,
            )
        )
        for intersection, wait_time in fairness_plan:
            print(f"  {intersection}: Wait Time {wait_time}")

        time.sleep(1)


if __name__ == "__main__":
    simulation_loop(steps=5, scenario="rush_hour")
