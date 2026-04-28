# 🌐 ARP Poisoning & Man-in-the-Middle (MitM) Simulation

This repository contains a Python-based implementation of an ARP Spoofing attack, developed for educational purposes to demonstrate how the Address Resolution Protocol (ARP) can be manipulated within a local network.

> ⚠️ This project is intended strictly for use in controlled lab environments.

---

## 🔍 Overview

ARP Spoofing is a technique in which an attacker sends forged ARP messages within a local network to associate their MAC address with the IP address of another host (typically the default gateway).

This allows the attacker to intercept, monitor, and potentially modify network traffic, effectively positioning themselves as a **Man-in-the-Middle (MitM)**.

---

## 🚀 Features

* Bi-directional ARP poisoning (victim ↔ router)
* Automatic IPv4 forwarding management to maintain connectivity
* Graceful network restoration after interruption (Ctrl + C)
* Real-time packet counter for monitoring attack activity

---

## 🛠️ Requirements

* Linux-based OS (Kali Linux or Parrot OS recommended)
* Python 3.x
* Scapy library

Install dependencies:

```bash id="w2zv7n"
pip install scapy
```

> ⚠️ Root privileges are required to craft and send raw packets.

---

## ⚙️ Configuration

Before running the script, update the following variables with your lab environment details:

```python id="n9q3xt"
VICTIM_IP = "..."
VICTIM_MAC = "..."

ROUTER_IP = "..."
ROUTER_MAC = "..."

ATTACKER_MAC = "..."
```

---

## 📋 Usage

### 1. Run the Script

```bash id="b8g4kl"
sudo python3 arp_spoofer.py
```

---

### 2. Monitor the Traffic

Use Wireshark on the attacker machine to observe intercepted traffic flowing between the victim and the router.

---

## 📖 How It Works

The script performs the following steps:

1. Sends forged ARP replies to the victim (spoofing the router)
2. Sends forged ARP replies to the router (spoofing the victim)
3. Enables IP forwarding to relay traffic transparently
4. Maintains the poisoned state by continuously sending packets
5. Restores the original ARP tables upon termination

---

## 🧪 Learning Objectives

This project helps develop understanding of:

* The stateless nature of the ARP protocol
* Lack of authentication in ARP communications
* Kernel-level network forwarding (`sysctl`)
* Real-world MitM attack mechanics
* Defensive measures such as:

  * Dynamic ARP Inspection (DAI)
  * Static ARP entries
  * Network segmentation

---

## 🛡️ Security Notice

This tool is intended for educational and authorized testing only.

* Do not use on networks without explicit permission
* Unauthorized interception of network traffic is illegal
* Always operate within a controlled lab environment

---

## 📈 Future Improvements

* Add packet sniffing and logging capabilities
* Integrate basic traffic filtering
* Support automated network discovery
* Implement detection/defense simulation

---

## ❗ Disclaimer

This project is part of a cybersecurity learning path focused on ethical hacking and defensive awareness.

All experiments were conducted in isolated lab environments.
The author does not support or condone misuse of this tool.

---

## 📄 License

This project is released under the MIT License.
