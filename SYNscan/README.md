# SYN Scan & Network Reconnaissance Analysis Lab

![Recon](https://img.shields.io/badge/Phase-Reconnaissance-red?style=for-the-badge)
![Network](https://img.shields.io/badge/Network-TCP_Scanning-orange?style=for-the-badge)
![SOC](https://img.shields.io/badge/SOC-Detection-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Tool-Python-yellow?style=for-the-badge)

---

## 🧠 Overview

This project simulates TCP SYN scanning techniques used in network reconnaissance phases of cyber attacks.

The objective is to understand how attackers identify open services on target systems and how these behaviors are detected and mitigated from a SOC perspective.

---

## ⚔️ What is SYN Scanning

A SYN scan is a network reconnaissance technique that exploits the TCP three-way handshake:

1. SYN packet is sent to a target port
2. If the port is open, a SYN-ACK is returned
3. If closed, an RST response is received

This allows attackers to map active services without fully establishing a TCP connection.

---

## 🧪 Technical Behavior

This implementation demonstrates:

- TCP SYN packet generation
- Port scanning over a target range
- Response analysis (SYN-ACK vs RST)
- Identification of open, closed, and filtered ports

---

## 🧠 Why It Matters

SYN scanning is widely used in:

- Network reconnaissance
- Attack surface mapping
- Pre-exploitation intelligence gathering

Because it does not complete the TCP handshake, it is considered a “stealthier” scanning technique compared to full connection scans.

---

## 🛰️ SOC & Detection Perspective

From a defensive standpoint, SYN scanning is a common early-stage attack indicator.

### 📊 Network Indicators:
- High volume of SYN packets to multiple ports
- Unusual sequential or randomized port probing
- No corresponding completion of TCP sessions

### 🖥 Detection Methods:
- IDS/IPS signatures (e.g. Suricata, Snort)
- Rate-based anomaly detection
- NetFlow traffic pattern analysis
- Firewall logging of repeated half-open connections

---

## 🛡 Mitigation Strategies

To reduce exposure to SYN scanning:

- Enable SYN flood protection mechanisms
- Use rate limiting on incoming connections
- Deploy IDS/IPS systems
- Monitor abnormal port scanning patterns
- Restrict unnecessary open services

---

## 📁 Project Structure

```text
SYNscan/
├── syn_scan.py
└── README.md
```

---

## 🧠 Key Learning Outcomes

- TCP handshake exploitation for reconnaissance
- Difference between full connect vs SYN scanning
- Network traffic analysis fundamentals
- SOC detection techniques for early-stage attacks
- Understanding attacker reconnaissance workflows

---

## 📌 Disclaimer

This project is intended for educational and cybersecurity research purposes in controlled environments only.

---

## 🏷️ Tags

`SYN Scan` · `Network Reconnaissance` · `TCP/IP` · `SOC Detection` · `IDS/IPS` · `Cybersecurity Lab`
