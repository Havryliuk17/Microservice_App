#!/usr/bin/env python3

import subprocess
import time
import requests
import sys
import os
from dotenv import load_dotenv

load_dotenv()
DB_PORT = 8001
BL_PORT = 8002
CLIENT_PORT = 8000

DB_URL = f"http://localhost:{DB_PORT}"
BL_URL = f"http://localhost:{BL_PORT}"
CLIENT_URL = f"http://localhost:{CLIENT_PORT}"


def wait_for_service(name, base_url, timeout=30):
    """
    Polls the /health endpoint until a 200 response or timeout occurs.
    """
    start_time = time.time()
    health_url = f"{base_url}/health"
    while time.time() - start_time < timeout:
        try:
            r = requests.get(health_url, timeout=2)
            if r.status_code == 200:
                print(f"{name} is up!")
                return
        except requests.exceptions.RequestException:
            pass
        time.sleep(1)
    print(f"ERROR: {name} was not ready after {timeout} seconds.")
    sys.exit(1)

def main():
    print("=== Starting Database Service ===")
    db_proc = subprocess.Popen([
        "uvicorn", "db_service:app",
        "--port", str(DB_PORT),
        "--host", "0.0.0.0",
        "--reload"
    ])

    print("=== Starting Business Logic Service ===")
    bl_proc = subprocess.Popen([
        "uvicorn", "business_service:app",
        "--port", str(BL_PORT),
        "--host", "0.0.0.0",
        "--reload"
    ])

    print("=== Starting Client Service ===")
    client_proc = subprocess.Popen([
        "uvicorn", "client_service:app",
        "--port", str(CLIENT_PORT),
        "--host", "0.0.0.0",
        "--reload"
    ])

    print("\nWaiting for services to be ready...")
    wait_for_service("Database Service", DB_URL, timeout=30)
    wait_for_service("Business Logic Service", BL_URL, timeout=30)
    wait_for_service("Client Service", CLIENT_URL, timeout=30)

    print("\n=== All services are running! ===\n")



if __name__ == "__main__":
    main()
