# 🔁 Basic Python Remote Command Execution Lab (Client-Server Socket Model)

This project demonstrates a **fundamental client-server architecture** for remote command execution using Python’s standard networking libraries.

It is designed for educational purposes to explore how TCP-based remote communication and process execution work at a low level.

---

## 🔍 Overview

The system consists of two components:

### 🖥️ `listener.py` (Server Node)

* Acts as the central control interface
* Waits for incoming TCP connections
* Receives and processes remote command outputs
* Provides an interactive command interface

---

### 💻 `main.py` (Client Node)

* Runs on the target machine
* Establishes a connection back to the server
* Executes received commands locally
* Sends command output back to the server

---

## 🛠 Features

### 🌐 TCP Socket Communication

Uses Python’s `socket` module to establish a reliable stream-based connection between client and server.

---

### 📁 Dynamic Directory Tracking

* Client tracks working directory using `os.getcwd()`
* Server receives updates to maintain session context
* Ensures synchronized command-line experience

---

### ⚙️ System Command Execution

* Uses `subprocess.run()` for command execution
* Captures both:

  * Standard Output (stdout)
  * Standard Error (stderr)

---

### 📂 Persistent Directory Handling

* Implements custom `cd` logic using `os.chdir()`
* Maintains state across multiple command executions

---

## 🚀 Lab Setup & Usage

### 📦 Requirements

* Python 3.x
* Same network or reachable IP connectivity between machines

---

### ▶️ Step 1 — Configure Client

Edit `main.py` and set the server IP:

```python id="k2m8vp"
SERVER_IP = "192.168.1.XX"
```

---

### ▶️ Step 2 — Start Server (Listener)

On the control machine:

```bash id="x7c4ql"
python3 listener.py
```

The server will start listening on port **8080**.

---

### ▶️ Step 3 — Start Client

On the target machine:

```bash id="m9n3vz"
python3 main.py
```

---

### 💻 Interaction

Once connected:

* Commands typed on the server are executed on the client
* Output is returned in real time
* Use `exit` to terminate the session safely

---

## 🧠 Learning Objectives

This project demonstrates:

* TCP client-server architecture fundamentals
* Remote process execution using Python
* Standard output/error redirection
* Session state synchronization over network
* Basic design of remote administration workflows

---

## 🧪 Educational Context

This implementation helps understand:

* How remote command systems are structured
* How data is transmitted over TCP sockets
* How operating systems execute external processes
* How state is preserved across distributed systems

---

## ⚠️ Security Disclaimer

This project is intended strictly for **educational and authorized cybersecurity research**.

* Do not execute on unauthorized systems
* Use only in isolated lab environments
* Unauthorized remote execution is illegal

---

## 📄 License

This project is released under the MIT License.
