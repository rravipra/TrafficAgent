# Multi-Agent Traffic Management Simulation

This project simulates a multi-agent system for real-time urban traffic management. It demonstrates how various AI-powered agents collaborate to reduce congestion and improve emergency vehicle response times. The system includes agents for traffic signal control, routing, incident detection, fairness, smart vehicle communication, and drone surveillance. Vehicles are modeled as objects that can update their status (e.g., switching modes) based on input from the agents.

## Overview

**Agents:**
- **TrafficSignalAgent (AI_AGENT_1):** Adjusts traffic signals using real-time data and an online ML model (with periodic retraining).
- **RoutingAgent (AI_AGENT_2):** Provides routing recommendations based on current traffic conditions.
- **IncidentAgent (AI_AGENT_3):** Detects incidents (e.g., accidents) by monitoring low-speed traffic.
- **FairnessAgent (AI_AGENT_4):** Tracks wait times at intersections to ensure fair signal distribution.
- **SmartVehicleAgent (AI_AGENT_5):** Simulates smart vehicle communication and sends updates to vehicles so they can adjust their operating modes.
- **DroneAgent (AI_AGENT_6):** Simulates drones performing aerial surveillance to detect congestion, emergencies, and approach directions.
- **Vehicle Class:** Represents individual vehicles (with attributes like smart capability, mode, location, and associated intersection) that can update their status.

## Prerequisites

- **Python 3.7+**
- **TomTom API Key:** Obtain your API key from the [TomTom Developer Portal](https://developer.tomtom.com/).
- **VSCode (Optional):** For development and debugging.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone <repository_url>
   cd <repository_directory>
Create a Virtual Environment:

Open the integrated terminal in VSCode (or your preferred terminal) and run:

bash
Copy
python -m venv venv
Activate the Virtual Environment:

On Windows (Command Prompt):

bash
Copy
.\venv\Scripts\activate
On Windows (PowerShell):

powershell
Copy
.\venv\Scripts\Activate.ps1
On macOS/Linux:

bash
Copy
source venv/bin/activate
You should see (venv) at the beginning of your terminal prompt.

Install Dependencies:

With the virtual environment activated, run:

bash
Copy
pip install -r requirements.txt
Configuration
Setting Up the API Key
Obtain a TomTom API Key:

Sign up at the TomTom Developer Portal and create an API key.

Create a .env File:

In the project root, create a file named .env and add your API key:

env
Copy
API_KEY=your_actual_api_key_here
Configure config.py:

Ensure config.py loads the API key from the .env file. Your config.py should look similar to this:

python
Copy
import os
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env

API_KEY = os.getenv("API_KEY")
DATA_FILE = 'traffic_data.csv'
LAST_RETRAIN_FILE = 'last_retrain.txt'
RETRAIN_INTERVAL_SECONDS = 3600 * 24 * 14
Security:

The provided .gitignore file ignores both .env (and optionally config.py) so that your API key isn’t committed to version control.

Project Structure
arduino
Copy
project/
├── README.md
├── .gitignore
├── requirements.txt
├── config.py
├── simulation.py
└── agents
    ├── __init__.py
    ├── traffic_signal_agent.py
    ├── routing_agent.py
    ├── incident_agent.py
    ├── fairness_agent.py
    ├── smart_vehicle_agent.py
    ├── drone_agent.py
    └── vehicle.py
Running the Simulation
Via Terminal
Activate the Virtual Environment.

Run the simulation:

bash
Copy
python simulation.py
Using VSCode
Select the Virtual Environment Interpreter:

Open the Command Palette (Ctrl+Shift+P or Cmd+Shift+P on macOS).

Choose Python: Select Interpreter and select the one from your venv.

Configure Debugging (Optional): Create a launch.json file with the following configuration:

json
Copy
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Simulation",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/simulation.py",
            "console": "integratedTerminal",
            "envFile": "${workspaceFolder}/.env"
        }
    ]
}
Run/Debug: Press F5 or click the Run icon to start the simulation.

How It Works
Traffic Signal Control:
The TrafficSignalAgent uses live (or simulated) traffic data, calculates congestion, predicts future congestion with an online ML model, and adjusts signal timings accordingly. It also retrains periodically using historical data.

Routing and Incident Detection:
The RoutingAgent and IncidentAgent make decisions based on current traffic conditions.

Smart Vehicles:
The Vehicle class represents each vehicle. Smart vehicles communicate their status via SmartVehicleAgent, which also sends updates (such as routing recommendations or mode changes). For instance, if a vehicle’s wait time is high, it might switch to eco-mode; emergency vehicles trigger signal overrides based on approach direction provided by the DroneAgent.

Drone Surveillance:
The DroneAgent simulates aerial scans to detect emergencies and determines the approach direction (e.g., "N", "S", "E", "W") for emergency vehicles.

Fairness:
The FairnessAgent tracks intersection wait times to ensure equitable traffic signal distribution.

The simulation outputs color-coded, formatted text in the terminal. Signal light statuses are displayed with colored emojis (🟢, 🟡, 🔴) and clear messages from each agent.

License
This project is licensed under the MIT License.
