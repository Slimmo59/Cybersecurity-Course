# 🧵 Multi-Threaded Distributed Task Execution System (Educational Simulation)

This project implements a **multi-threaded client-server architecture** designed to simulate distributed task execution across multiple connected nodes in a controlled environment.

It demonstrates how a central server can distribute scripts or workloads to multiple clients for execution and analysis purposes.

---

## 🛠 Components

### 🖥️ `trojan_execution_server.py`

* Multi-threaded TCP server using `socketserver.ThreadingTCPServer`
* Handles multiple concurrent client connections
* Distributes a predefined task script (`command.sh`) to connected clients
* Validates script availability before transmission

---

### 💻 `trojan_execution_client.py`

* Client-side execution agent
* Connects to the server and retrieves task payloads
* Stores received script temporarily
* Grants execution permissions (`chmod 755`)
* Executes the script locally and cleans up after execution

---

### 📜 `command.sh`

* Sample Bash script used for **controlled load testing simulation**
* Designed to generate multiple HTTP requests to a local test environment
* Used to observe system behavior under stress conditions

---

## 🚀 How It Works

---

### 🖥️ Server Behavior

* Listens on a specified TCP port (default: `8000`)
* Accepts multiple simultaneous client connections
* Sends the script content to each connected client
* Returns error if payload is unavailable

---

### 💻 Client Behavior

* Connects to the server using IP and port
* Receives script payload over TCP
* Writes payload to a temporary file
* Executes script using system shell
* Removes temporary file after execution

---

### 📊 Task Execution Model

This system follows a **distributed execution workflow**:

1. Server defines workload
2. Clients request and receive task
3. Clients execute task locally
4. Temporary artifacts are cleaned up

---

## 📋 Usage

---

### 📦 Requirements

* Python 3.x
* Linux/Unix-based system for script execution
* `curl` installed (for test workload execution)

---

### ▶️ Step 1 — Start Server

```bash id="k7m3vp"
python3 trojan_execution_server.py
```

---

### ⚙️ Step 2 — Configure Task

Ensure `command.sh` is located in the server directory.

You can modify:

* Target endpoint
* Request count
* Execution delay

---

### 💻 Step 3 — Start Client

```bash id="x4n8ql"
sudo python3 trojan_execution_client.py <server_ip> 8000
```

Example:

```bash id="m9c3vz"
sudo python3 trojan_execution_client.py 127.0.0.1 8000
```

---

## 🧠 Learning Objectives

This project demonstrates:

* Multi-threaded server architectures
* Distributed task execution models
* Client-server file transfer over TCP
* Temporary file handling and cleanup strategies
* Process execution using Python (`subprocess`)
* Basic workload simulation in controlled environments

---

## 🧪 Educational Context

This system is intended to study:

* How distributed systems handle task delegation
* How remote execution pipelines are structured
* How clients process externally provided workloads
* How system behavior changes under simulated load conditions

---

## ⚠️ Security & Ethical Notice

This project is intended strictly for **educational and authorized testing environments**.

* Do not deploy on production systems
* Do not execute outside isolated lab environments
* Use only on systems you own or have explicit permission to test

---

## 📄 License

This project is released for educational and research purposes under the MIT License.
