# Multi-Agent Traffic Management System

This project simulates a multi-agent system for real-time traffic management by collaborating among:

- **TrafficSignalAgent (AI_AGENT_1):**  
  Uses live traffic data and an online ML model (with periodic retraining) to adjust traffic signal timings.
- **RoutingAgent (AI_AGENT_2):**  
  Provides vehicle routing recommendations based on current traffic conditions.
- **IncidentAgent (AI_AGENT_3):**  
  Detects incidents (e.g., accidents) by monitoring extremely low speeds.
- **FairnessAgent (AI_AGENT_4):**  
  Tracks wait times at intersections to ensure fair signal distribution.
- **SmartVehicleAgent (AI_AGENT_5):**  
  Simulates smart vehicles that communicate their status, including emergencies.
- **DroneAgent (AI_AGENT_6):**  
  Simulates drones providing aerial surveillance to detect congestion and emergencies.

## Project Structure
