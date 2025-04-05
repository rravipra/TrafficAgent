# agents/traffic_signal_agent.py

import requests
import json
import os
import csv
import pandas as pd
import numpy as np
from datetime import datetime
import random
from sklearn.linear_model import SGDRegressor

from config import API_KEY, DATA_FILE, LAST_RETRAIN_FILE, RETRAIN_INTERVAL_SECONDS


class TrafficSignalAgent:
    def __init__(self):
        self.online_model = SGDRegressor(max_iter=1000, tol=1e-3)
        self.online_model.partial_fit(np.array([[0.0, 1.0]]), np.array([0.0]))

    def fetch_traffic_data(self, lat, lon):
        url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/relative0/10/json"
        params = {"point": f"{lat},{lon}", "unit": "KMPH", "key": API_KEY}
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                print(
                    "Error fetching traffic data:", response.status_code, response.text
                )
        except Exception as e:
            print("Exception during API call:", e)
        return {
            "flowSegmentData": {
                "currentSpeed": random.randint(10, 60),
                "freeFlowSpeed": 60,
            }
        }

    def compute_congestion(self, current_speed, free_flow_speed):
        if free_flow_speed > 0:
            congestion = max(0, (free_flow_speed - current_speed) / free_flow_speed)
            return min(1, congestion)
        else:
            return 1.0

    def predict_future_congestion(self, features, actual_congestion):
        feature_vector = np.array(
            [features["current_speed"], features["free_flow_speed"]]
        )
        predicted = self.online_model.predict(feature_vector.reshape(1, -1))[0]
        self.online_model.partial_fit(
            feature_vector.reshape(1, -1), np.array([actual_congestion])
        )
        return min(1, max(0, predicted))

    def generate_signal_plan_output(
        self,
        intersection_id,
        congestion_estimates,
        signal_timings,
        agent_confidence=0.9,
        fairness_score=1.0,
    ):
        phase_plan = []
        for phase_id, green_duration in signal_timings.items():
            phase = {
                "phase_id": phase_id,
                "green_duration": green_duration,
                "yellow_duration": 5,
                "red_duration": max(90 - green_duration, 10),
                "priority": (
                    1
                    if congestion_estimates.get(phase_id.split("_")[0], 0) > 0.7
                    else 2
                ),
            }
            phase_plan.append(phase)

        signal_output = {
            "intersection_id": intersection_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "recommendation_source": "AI_AGENT_1",
            "phase_plan": phase_plan,
            "congestion_estimates": congestion_estimates,
            "fairness_score": fairness_score,
            "agent_confidence": agent_confidence,
        }
        return json.dumps(signal_output, indent=2)

    def build_signal_states(self, signal_plan_json, current_time=0):
        ns_green = None
        ew_green = None
        for phase in signal_plan_json["phase_plan"]:
            if "N_S" in phase["phase_id"]:
                ns_green = phase["green_duration"]
            elif "E_W" in phase["phase_id"]:
                ew_green = phase["green_duration"]
        if ns_green is None or ew_green is None:
            raise ValueError("Signal plan must contain both N_S and E_W phases.")

        ns_phase_duration = ns_green + 5
        ew_phase_duration = ew_green + 5
        total_cycle = ns_phase_duration + ew_phase_duration
        t = current_time % total_cycle

        def get_ns_state(t):
            if t < ns_green:
                return "GREEN", ns_green - t, "YELLOW"
            elif t < ns_phase_duration:
                return "YELLOW", ns_phase_duration - t, "RED"
            else:
                return "RED", total_cycle - t, "GREEN"

        def get_ew_state(t):
            if t < ns_phase_duration:
                return "RED", ns_phase_duration - t, "GREEN"
            elif t < ns_phase_duration + ew_green:
                return "GREEN", (ns_phase_duration + ew_green) - t, "YELLOW"
            else:
                return "YELLOW", total_cycle - t, "RED"

        ns_color, ns_time_remaining, ns_next_color = get_ns_state(t)
        ew_color, ew_time_remaining, ew_next_color = get_ew_state(t)

        signal_state = {
            "N": {
                "current_color": ns_color,
                "time_remaining": ns_time_remaining,
                "next_color": ns_next_color,
                "movements": {
                    "left": ns_color,
                    "straight": ns_color,
                    "right": ns_color,
                },
            },
            "S": {
                "current_color": ns_color,
                "time_remaining": ns_time_remaining,
                "next_color": ns_next_color,
                "movements": {
                    "left": ns_color,
                    "straight": ns_color,
                    "right": ns_color,
                },
            },
            "E": {
                "current_color": ew_color,
                "time_remaining": ew_time_remaining,
                "next_color": ew_next_color,
                "movements": {
                    "left": ew_color,
                    "straight": ew_color,
                    "right": ew_color,
                },
            },
            "W": {
                "current_color": ew_color,
                "time_remaining": ew_time_remaining,
                "next_color": ew_next_color,
                "movements": {
                    "left": ew_color,
                    "straight": ew_color,
                    "right": ew_color,
                },
            },
        }
        return signal_state

    def store_api_data(self, lat, lon, current_speed, free_flow_speed, congestion):
        file_exists = os.path.isfile(DATA_FILE)
        with open(DATA_FILE, mode="a", newline="") as csvfile:
            fieldnames = [
                "timestamp",
                "lat",
                "lon",
                "current_speed",
                "free_flow_speed",
                "congestion",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow(
                {
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "lat": lat,
                    "lon": lon,
                    "current_speed": current_speed,
                    "free_flow_speed": free_flow_speed,
                    "congestion": congestion,
                }
            )

    def retrain_model_from_data(self, csv_file=DATA_FILE):
        if not os.path.exists(csv_file):
            print("No historical data available for retraining.")
            return None
        data = pd.read_csv(csv_file)
        X = data[["current_speed", "free_flow_speed"]].values
        y = data["congestion"].values
        new_model = SGDRegressor(max_iter=1000, tol=1e-3)
        new_model.fit(X, y)
        print("Retrained model on historical data.")
        return new_model

    def check_and_retrain_model(self):
        current_time_ts = datetime.utcnow().timestamp()
        last_retrain_ts = 0
        if os.path.exists(LAST_RETRAIN_FILE):
            with open(LAST_RETRAIN_FILE, "r") as f:
                try:
                    last_retrain_ts = float(f.read().strip())
                except ValueError:
                    last_retrain_ts = 0
        if current_time_ts - last_retrain_ts > RETRAIN_INTERVAL_SECONDS:
            new_model = self.retrain_model_from_data()
            if new_model is not None:
                self.online_model = new_model
            with open(LAST_RETRAIN_FILE, "w") as f:
                f.write(str(current_time_ts))
            print("Model retrained at:", datetime.utcnow().isoformat() + "Z")
        else:
            next_retrain = last_retrain_ts + RETRAIN_INTERVAL_SECONDS
            print(
                "Next retraining scheduled at:",
                datetime.utcfromtimestamp(next_retrain).isoformat() + "Z",
            )

    def adjust_signals(self, lat, lon, current_time=0):
        traffic_data = self.fetch_traffic_data(lat, lon)
        flow_data = traffic_data.get("flowSegmentData", {})
        current_speed = flow_data.get("currentSpeed", 0)
        free_flow_speed = flow_data.get("freeFlowSpeed", 0)

        current_congestion = self.compute_congestion(current_speed, free_flow_speed)
        features = {"current_speed": current_speed, "free_flow_speed": free_flow_speed}
        predicted_congestion = self.predict_future_congestion(
            features, current_congestion
        )
        weighted_congestion = (current_congestion + predicted_congestion) / 2

        ns_green = int(30 + 30 * weighted_congestion)
        ew_green = int(30 + 30 * (1 - weighted_congestion))
        signal_timings = {"N_S_GREEN": ns_green, "E_W_GREEN": ew_green}

        congestion_estimates = {
            "N": weighted_congestion,
            "S": weighted_congestion,
            "E": 0.2,
            "W": 0.2,
            "predicted": {"N_S": predicted_congestion, "E_W": 0.2},
        }

        intersection_id = f"intersection_{lat}_{lon}"
        signal_plan_str = self.generate_signal_plan_output(
            intersection_id, congestion_estimates, signal_timings
        )
        signal_plan_json = json.loads(signal_plan_str)
        signal_state = self.build_signal_states(
            signal_plan_json, current_time=current_time
        )

        self.store_api_data(
            lat, lon, current_speed, free_flow_speed, current_congestion
        )
        self.check_and_retrain_model()

        return signal_state
