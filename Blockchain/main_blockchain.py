import requests
import json
import subprocess
import time
import os

def print_json(data):
    """Utility function to print JSON data in a readable format."""
    print(json.dumps(data, indent=4))

def run_simulation():
    # 1. Start the first node on port 8000
    # We use subprocess to run the node script as a separate background process
    print("[*] Starting Node 8000...")
    p8000 = subprocess.Popen(['python3', 'blockchain_8000.py'])
    time.sleep(3)  # Wait for the Flask server to initialize

    # 2. Check initial chain and send a transaction
    print("\n[*] Initial chain for Node 8000:")
    resp = requests.get("http://localhost:8000/chain")
    print_json(resp.json())

    # Example payload representing a real estate transaction
    payload_tx = {
        "id": "ID24",
        "canale": "Sales",
        "dati": "Villa Milan",
        "timestamp": "1689657144"
    }
    
    print("\n[*] Sending transaction to Node 8000...")
    requests.post("http://127.0.0.1:8000/transactions/new", json=payload_tx)

    # 3. Mining the block
    # Mining validates the pending transactions and adds a new block to the chain
    print("\n[*] Mining on Node 8000...")
    requests.get("http://localhost:8000/mine")

    # 4. Start the second node on port 8001
    print("\n[*] Starting Node 8001...")
    p8001 = subprocess.Popen(['python3', 'blockchain_8001.py'])
    time.sleep(3)

    # 5. Register Node 8000 on Node 8001
    # This step informs Node 8001 about the existence of Node 8000 in the network
    print("\n[*] Registering Node 8000 at Node 8001...")
    requests.post("http://127.0.0.1:8001/nodes/register", json={"node": "http://127.0.0.1:8000"})

    # 6. New transaction on Node 8001
    payload_tx2 = {
        "id": "ID26",
        "canale": "Sales",
        "dati": "Apartment Rome",
        "timestamp": "1689657199"
    }
    print("\n[*] Sending transaction to Node 8001...")
    requests.post("http://127.0.0.1:8001/transactions/new", json=payload_tx2)

    # 7. Conflict Resolution (Consensus)
    # Node 8001 checks if its neighbors (Node 8000) have a longer valid chain
    print("\n[*] Resolving conflicts on Node 8001...")
    requests.get("http://localhost:8001/nodes/resolve")

    # 8. Mining on Node 8001
    print("\n[*] Mining on Node 8001...")
    requests.get("http://localhost:8001/mine")

    # 9. Register Node 8001 on Node 8000 and final synchronization
    print("\n[*] Registering Node 8001 at Node 8000...")
    requests.post("http://127.0.0.1:8000/nodes/register", json={"node": "http://127.0.0.1:8001"})

    print("\n[*] Final consensus on Node 8000...")
    requests.get("http://localhost:8000/nodes/resolve")

    # 10. Show final results
    print("\n[*] FINAL CHAIN FOR NODE 8000:")
    final_resp = requests.get("http://localhost:8000/chain")
    print_json(final_resp.json())

    print("\n[*] Simulation completed. Closing processes...")
    # Terminate the background processes
    p8000.terminate()
    p8001.terminate()

if __name__ == "__main__":
    try:
        run_simulation()
    except KeyboardInterrupt:
        print("\nSimulation interrupted by user.")
    except Exception as e:
        print(f"\nAn error occurred during simulation: {e}")
