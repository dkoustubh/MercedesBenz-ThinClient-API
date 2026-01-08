# MercedesBenz ThinClient Display Project

## Author
**Koustubh Deodhar**

## Overview
This project is a Thin Client display system designed for Mercedes-Benz manufacturing lines. It visualizes real-time production data, key performance indicators (KPIs), and shift information.

## How It Works

### Architecture
The system consists of two main components:

1.  **Frontend (`ThinClientTestv2.html`)**:
    *   A lightweight, responsive HTML5/JS dashboard.
    *   Runs in any standard web browser (Thin Client optimized).
    *   Fetches data from the local Proxy Server to avoid CORS issues and simplify data aggregation.
    *   Displays Production counts, OEE (Overall Equipment Effectiveness), MTBF/MTTR, and breakdown status.

2.  **Proxy Server (`proxy_server.py`)**:
    *   A Python-based intermediate server (using Flask or simple HTTP handling).
    *   Acts as a gateway between the Thin Client and the internal Manufacturing Execution System (MES) APIs.
    *   Handles authentication and network request routing.

### Data Flow
1.  The **Frontend** requests data (e.g., `/api/production`) from `http://localhost:8000`.
2.  The **Proxy Server** intercepts this request.
3.  The **Proxy Server** forwards the request to the upstream Mercedes-Benz internal API (e.g., `http://172.18.2.39:5000/...`).
4.  The response is relayed back to the Frontend for display.

## How to Fetch APIs
To integrate or modify the API data, check the `proxy_server.py` file.

**Key Endpoints:**
The proxy exposes local endpoints that map to the underlying system:
*   **Get Shift Production Data**: Fetches current counts (Target, Actual, Gap).
*   **Get Line Status**: checks if the line is running or stopped.

**Example Usage (Python)**:
```python
import requests

# Example: Fetching production data via the proxy
response = requests.get("http://localhost:8000/get_production_data")
data = response.json()
print(data)
```

## Setup & Running
1.  **Start the Proxy Server**:
    ```bash
    python proxy_server.py
    ```
2.  **Open the Display**:
    Open `ThinClientTestv2.html` in your web browser.

## Technologies
*   **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
*   **Backend**: Python