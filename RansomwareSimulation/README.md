# 🔐 Remote Encryption & Incident Response Simulation Lab (Educational PoC)

This repository contains a **Proof of Concept (PoC)** designed to simulate the technical behavior of a remote file encryption scenario in a controlled environment.

The project is intended for educational purposes to help understand **Command & Control (C2) communication**, **symmetric encryption workflows**, and **incident response behaviors** in compromised systems.

---

## 🎓 Educational Objectives

This lab focuses on understanding:

* **Command & Control (C2) Architecture**
  How remote systems can receive and execute structured instructions

* **Symmetric Encryption Systems**
  Use of Fernet (AES-based encryption) for secure data transformation

* **Network Communication**
  Persistent TCP connections and basic multi-threaded socket handling

* **Security Incident Simulation**
  Behavioral artifacts such as file modification indicators and warning notes

---

## 🛠️ Project Components

### 🖥️ Controller (`controller.py`)

Acts as the central management interface.

Responsibilities:

* Establishes TCP connection with the target node
* Generates a session encryption key
* Provides an interactive CLI for remote operations
* Sends structured commands to the connected node

---

### 💻 Worker Node (`victim.py`)

Simulated endpoint system in a controlled environment.

Responsibilities:

* Listens for incoming controller connections
* Handles requests using multi-threaded processing
* Recursively processes target directories
* Applies encryption or decryption operations
* Generates or removes a simulated incident indicator file

---

## 🚀 Lab Setup & Execution

### 📦 Prerequisites

* Python 3.x
* cryptography library

Install dependency:

```bash id="q9m2xp"
pip install cryptography
```

---

### 🧪 Step 1 — Start Worker Node

Run on the target system (e.g., Linux VM):

```bash id="k3n8vz"
python3 victim.py
```

The node will start listening on port **8080**.

---

### 🧪 Step 2 — Start Controller

Run on the control system:

```bash id="m7c4ql"
python3 controller.py
```

Enter the IP address of the worker node to establish a connection.

---

### ⚙️ Available Operations

* **Encryption Mode**
  Select a target directory to simulate file encryption on the remote system

* **Decryption Mode**
  Restore previously modified files using the same session key

---

## 📖 Learning Outcomes

This project demonstrates:

* Fundamentals of C2 communication models
* Practical implementation of symmetric cryptography (Fernet / AES)
* Remote task execution over TCP sockets
* File system traversal and batch processing
* Basic simulation of security incident workflows

---

## 🧪 Recommended Environment

This project should only be executed in:

* Isolated virtual machines
* Cybersecurity training labs
* Controlled test networks (e.g., Metasploitable environments)

---

## ⚠️ Legal & Ethical Disclaimer

This project is intended strictly for **educational and research purposes only**.

* Do not use on systems without explicit authorization
* Unauthorized execution on real systems is illegal
* Always operate within controlled lab environments

---

## 📄 License

This project is released under the MIT License.
