# 🚦 Multi-Agent Traffic Management System

A multi-agent system for intelligent traffic signal control, smart vehicle communication, emergency response, and fairness enforcement in urban traffic simulation.

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository_url>
cd <repository_directory>
```

### 2. Create and Activate a Virtual Environment
Create the environment:

```bash
Copy
python -m venv venv
```

### 3. Activate the environment:

On Windows (Command Prompt):

```bash
Copy
.\venv\Scripts\activate
```

On Windows (PowerShell):

```powershell
Copy
.\venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
Copy
source venv/bin/activate
```

You should see (venv) at the beginning of your terminal prompt.

### 4. Install Dependencies

```bash
Copy
pip install -r requirements.txt
```

🔐 Configuration
Setting Up the API Key
Obtain a TomTom API Key:
Sign up at the TomTom Developer Portal and generate an API key.

Create a .env File:
In the project root, create a file named .env:

env
Copy
API_KEY=your_actual_api_key_here
Configure config.py:
Ensure config.py looks like this:

```python
Copy
import os
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env

API_KEY = os.getenv("API_KEY")
DATA_FILE = 'traffic_data.csv'
LAST_RETRAIN_FILE = 'last_retrain.txt'
RETRAIN_INTERVAL_SECONDS = 3600 * 24 * 14
```

✅ The provided .gitignore file is already set up to exclude .env and (optionally) config.py to keep your API key secure.

📁 Project Structure
```plaintext
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
```

▶️ Running the Simulation
Via Terminal
Activate the virtual environment.

Run the simulation:

```bash
Copy
python simulation.py
```

Using VSCode
Open the Command Palette (Ctrl+Shift+P or Cmd+Shift+P on macOS).

Select Python: Select Interpreter and choose the one from your venv.

(Optional) Create a launch.json for debugging:

```json
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
```

Press F5 or click the Run icon to start the simulation.
