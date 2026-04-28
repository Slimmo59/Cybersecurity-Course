# 🔐 RSA Remote Decryption Service (Python Sockets)

This project implements a **client-server architecture** designed to demonstrate remote RSA decryption and binary data exchange over TCP/IP sockets.

It focuses on combining **network programming** with **asymmetric cryptography using OpenSSL**.

---

## 📌 Project Overview

The system enables a client to send RSA-encrypted binary data to a remote server, which then decrypts the content using a private key and returns the plaintext result.

---

## 🧩 Components

### 🖥️ `server_sender_key.py`

* TCP server that listens for incoming encrypted data
* Uses RSA private key for decryption
* Returns decrypted plaintext back to the client

---

### 💻 `client_sender_key.py`

* Reads encrypted binary files (`cipher.bin`)
* Sends data over TCP to the server
* Receives decrypted output and stores it locally

---

### 🔑 `pub_priv_pair.key`

* RSA private key used by the server
* Required for decryption operations

---

### 📦 `cipher.bin`

* Sample RSA-encrypted binary file
* Used to test communication and decryption flow

---

## 🛠 Cryptographic Details

### 🔐 RSA Key Usage

The server relies on an RSA private key to decrypt incoming payloads.

> ⚠️ The included key is for educational purposes only and must not be used in production systems.

---

### 📁 Encrypted Data Format

The cipher file contains RSA-encrypted binary data that is unreadable without the corresponding private key and decryption process.

---

## 🚀 Generating Your Own Keys

You can generate your own RSA keypair and encrypted files using OpenSSL:

---

### 🔑 Generate RSA Private Key

```bash id="k9m2vp"
openssl genrsa -out pub_priv_pair.key 1024
```

---

### 📤 Extract Public Key

```bash id="x4n7ql"
openssl rsa -in pub_priv_pair.key -pubout -out public_key.pem
```

---

### 📦 Create Encrypted File

Create a sample message:

```bash id="c2m8xz"
echo "This is a secret message" > secret.txt
```

Encrypt it using the public key:

```bash id="p7n4vt"
openssl pkeyutl -encrypt -pubin -inkey public_key.pem -in secret.txt -out cipher.bin -pkeyopt rsa_padding_mode:oaep
```

---

## 💻 Usage Instructions

### 1. Start the Server

Place `server_sender_key.py` and `pub_priv_pair.key` in the same directory:

```bash id="m3q8xn"
python3 server_sender_key.py
```

The server will start listening on port **8082**.

---

### 2. Run the Client

Ensure `cipher.bin` is available, then run:

```bash id="r8c2vp"
python3 client_sender_key.py <SERVER_IP> 8082
```

After execution, the decrypted result will be saved as:

```
plainD.txt
```

---

## 📖 Learning Objectives

This project demonstrates:

* Client-server architecture using Python sockets
* Binary data transmission over TCP/IP
* RSA asymmetric encryption workflow
* Integration between Python and OpenSSL
* Secure key-based decryption systems
* File handling in networked environments

---

## 🧪 Recommended Environment

This project is intended for use in:

* Virtualized lab environments
* Cybersecurity training setups
* Isolated network simulations

---

## ⚠️ Security Disclaimer

This project is provided for **educational and research purposes only**.

* Do not expose private keys in real environments
* Do not use outside controlled labs
* Unauthorized decryption of data is illegal

---

## 📄 License

This project is released under the MIT License.
