# 🏠 Decentralized Real Estate Blockchain Simulation

This project implements a peer-to-peer (P2P) blockchain network designed to simulate real estate transactions in a decentralized environment.

It includes a distributed ledger, Proof of Work (PoW) mining, and a consensus mechanism to ensure consistency across multiple nodes.

> ⚠️ This project is intended for educational and simulation purposes only.

---

## 📂 Project Structure

* `blockchain_8000.py`, `blockchain_8001.py`, `blockchain_8003.py`
  → Individual blockchain nodes (Flask servers)

* `main_blockchain.py`
  → Orchestrator script to automate the simulation and demonstrate network behavior

---

## ⚙️ Core Features

* **Proof of Work (PoW)**
  Blocks require solving a computational puzzle before being added to the chain

* **Consensus Algorithm (Longest Chain Rule)**
  Nodes automatically resolve conflicts by adopting the longest valid chain

* **Immutable Ledger**
  Each block contains the SHA-256 hash of the previous block, ensuring integrity

* **REST API Interface**
  Each node exposes endpoints for interaction and testing

---

## 🔌 API Endpoints

* `GET /mine`
  → Mine a new block

* `POST /transactions/new`
  → Add a new real estate transaction

* `GET /chain`
  → Retrieve the full blockchain

* `POST /nodes/register`
  → Register peer nodes

* `GET /nodes/resolve`
  → Trigger consensus across the network

---

## 🛠️ Requirements

* Python 3.x
* Flask
* Requests

Install dependencies:

```bash id="y7k2vm"
pip install Flask requests
```

---

## 🚀 Getting Started

### Run the Full Simulation

```bash id="q4r8ls"
python3 main_blockchain.py
```

This will automatically:

* Start multiple nodes (8000, 8001)
* Submit a transaction
* Mine a block
* Register nodes with each other
* Demonstrate consensus synchronization

---

## 🧪 Manual Execution

Run nodes manually in separate terminals:

```bash id="f8c3xp"
# Terminal 1
python3 blockchain_8000.py

# Terminal 2
python3 blockchain_8001.py
```

Then interact using Postman or cURL:

```bash id="r2m9zn"
http://localhost:8000/transactions/new
```

---

## 📝 Example Transaction

```json id="p5d1kt"
{
    "id": "REF-101",
    "canale": "Sales",
    "dati": "Luxury Penthouse in Rome",
    "timestamp": "1713360000"
}
```

---

## 📖 How It Works

1. Nodes maintain independent copies of the blockchain
2. Transactions are submitted via REST API
3. Mining creates new blocks using Proof of Work
4. Nodes communicate and share chain data
5. Consensus resolves conflicts using the longest chain rule

---

## 🧪 Learning Objectives

This project helps demonstrate:

* Fundamentals of blockchain architecture
* Peer-to-peer network communication
* Consensus mechanisms in distributed systems
* API-based interaction between nodes
* Data integrity using cryptographic hashing

---

## 🔐 Future Improvements

* Add authentication between nodes (mTLS)
* Improve transaction validation logic
* Implement digital signatures for transactions
* Add persistence (database instead of in-memory chain)
* Enhance security against malicious nodes

---

## 🛡️ Security Note

This simulation does not include authentication or encryption by default.

It is intentionally simplified to demonstrate blockchain concepts and should not be considered production-ready.

---

## 📄 License

This project is released under the MIT License.
