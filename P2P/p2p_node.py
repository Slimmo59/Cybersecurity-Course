#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P2P Chat Node - Stable FIX Version (Improved EXEC management)
Professional English Version for Kali/Ubuntu
"""

import socket
import threading
import sys
import subprocess
import shlex
import os
import time

class P2PNode:
    def __init__(self, listen_port: int) -> None:
        self.listen_host = "0.0.0.0"
        self.listen_port = listen_port
        self.server_socket: socket.socket | None = None
        self.peers: dict[tuple[str, int], socket.socket] = {}
        self.peers_lock = threading.Lock() # Ensures thread safety when managing connections
        self.running = True

    def start(self) -> None:
        """Initializes the server socket to listen for incoming peer connections."""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.listen_host, self.listen_port))
            self.server_socket.listen(5)
        except OSError as e:
            print(f"[ERROR] Could not start node on {self.listen_host}:{self.listen_port} -> {e}")
            sys.exit(1)

        print(f"[INFO] Node listening on {self.listen_host}:{self.listen_port}")

        # Start the background thread to accept connections
        listener = threading.Thread(target=self._listen_loop, name="ListenerThread", daemon=True)
        listener.start()

    def _listen_loop(self) -> None:
        """Continuously accepts incoming TCP connections."""
        while self.running:
            try:
                client_socket, client_address = self.server_socket.accept()
            except OSError:
                break

            print(f"\n[INCOMING CONNECTION] from {client_address[0]}:{client_address[1]}")

            with self.peers_lock:
                self.peers[client_address] = client_socket

            # Spawn a dedicated thread for each connected peer
            handler = threading.Thread(
                target=self._handle_peer,
                args=(client_socket, client_address),
                name=f"PeerHandler-{client_address}",
                daemon=True,
            )
            handler.start()

    def _handle_peer(self, peer_socket: socket.socket, peer_address: tuple[str, int]) -> None:
        """Handles communication logic: receives messages, file uploads, or execution requests."""
        try:
            while self.running:
                data = peer_socket.recv(8192)
                if not data:
                    break

                # === BINARY UPLOAD HANDLER ===
                if data.startswith(b"UPLOAD:"):
                    try:
                        header_end = data.find(b"\n") + 1
                        header = data[:header_end].decode("utf-8", errors="ignore")
                        size = int(header.split(":")[-1].strip())
                        file_data = data[header_end:]
                        self._receive_file(peer_socket, file_data, size, peer_address)
                        continue
                    except Exception as e:
                        print(f"[ERROR] Invalid UPLOAD format: {e}")
                        continue

                # === MESSAGE PARSING ===
                raw = data.decode("utf-8", errors="replace").strip()

                if raw.startswith("EXEC:"):
                    # Robust parsing for remote command execution
                    parts = raw.split(":", 2)
                    if len(parts) >= 3:
                        _, target, cmd = parts
                        print(f"\n[REMOTE EXEC from {peer_address[0]}:{peer_address[1]}] {cmd}")
                        self._execute_command(cmd, peer_socket, peer_address)
                    else:
                        print(f"\n[MALFORMED EXEC from {peer_address}] {raw}")
                else:
                    # Standard Chat Message
                    print(f"\n[MSG from {peer_address[0]}:{peer_address[1]}] {raw}")
                    # Auto-reply in uppercase (Echo service logic)
                    if raw and raw != raw.upper():
                        try:
                            peer_socket.sendall(raw.upper().encode("utf-8"))
                        except OSError:
                            break

        except (ConnectionResetError, OSError, Exception):
            pass
        finally:
            self._remove_peer(peer_address)

    def _execute_command(self, cmd: str, peer_socket: socket.socket, peer_address: tuple[str, int]):
        """Executes a shell command and sends the output back to the requester."""
        try:
            # Basic security filter
            dangerous = ["rm -rf", "dd if=", "> /dev/", "mkfs", "shutdown", "reboot", "rm -r", "format"]
            if any(kw in cmd.lower() for kw in dangerous):
                output = "[SECURITY ERROR] Command blocked for safety."
            else:
                exec_list = shlex.split(cmd)
                result = subprocess.run(
                    exec_list,
                    capture_output=True,
                    text=True,
                    timeout=60,
                    cwd="/tmp"
                )
                output = result.stdout + result.stderr
                if not output.strip():
                    output = f"[OK] Executed (exit code: {result.returncode})"
                else:
                    output = f"[OUTPUT]\n{output}"
        except subprocess.TimeoutExpired:
            output = "[ERROR] Execution timed out (60s)"
        except FileNotFoundError:
            output = f"[ERROR] Command not found: {cmd}"
        except Exception as e:
            output = f"[ERROR] {type(e).__name__}: {e}"

        try:
            peer_socket.sendall(output.encode("utf-8"))
        except OSError:
            pass

    def _receive_file(self, peer_socket: socket.socket, received_data: bytes, size: int, peer_address: tuple[str, int]):
        """Receives a binary file and saves it as an executable script in /tmp."""
        try:
            data = received_data
            while len(data) < size:
                chunk = peer_socket.recv(min(8192, size - len(data)))
                if not chunk:
                    break
                data += chunk

            save_path = "/tmp/command.sh"
            with open(save_path, "wb") as f:
                f.write(data)
            os.chmod(save_path, 0o755) # Make the script executable

            print(f"[UPLOAD SUCCESS] Script saved to /tmp/command.sh ({len(data)} bytes)")
            peer_socket.sendall(b"[OK] Script saved and marked as executable")
        except Exception as e:
            print(f"[ERROR] Saving script failed: {e}")

    # ====================== CLIENT-SIDE LOGIC ======================
    def connect_to_peer(self, ip: str, port: int) -> None:
        """Initiates a TCP connection to a remote node."""
        peer_address = (ip, port)
        with self.peers_lock:
            if peer_address in self.peers:
                print(f"[INFO] Already connected to {ip}:{port}")
                return

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(peer_address)
            with self.peers_lock:
                self.peers[peer_address] = sock
            print(f"[INFO] Connected to {ip}:{port}")

            handler = threading.Thread(target=self._handle_peer, args=(sock, peer_address), daemon=True)
            handler.start()
        except Exception as e:
            print(f"[ERROR] Connection failed: {e}")

    def _send_to_all(self, payload: str) -> None:
        """Broadcasts a payload to all connected peers."""
        encoded = payload.encode("utf-8")
        dead = []
        with self.peers_lock:
            for addr, sock in self.peers.items():
                try:
                    sock.sendall(encoded)
                except OSError:
                    dead.append(addr)
        for addr in dead:
            self._remove_peer(addr)

    def exec_on_peer(self, target: str, command: str) -> None:
        """Sends an execution request to a specific peer or 'all'."""
        with self.peers_lock:
            peer_list = list(self.peers.items())

        if not peer_list:
            print("[INFO] No peers connected.")
            return

        if target.lower() == "all":
            print(f"[EXEC] Running '{command}' on ALL peers...")
            self._send_to_all(f"EXEC:all:{command}")
            return

        try:
            idx = int(target) - 1
            if idx < 0 or idx >= len(peer_list):
                print(f"[ERROR] Peer index {target} out of range.")
                return
            addr, sock = peer_list[idx]
            print(f"[EXEC] Running on peer {idx+1} ({addr[0]})...")
            sock.sendall(f"EXEC:all:{command}".encode("utf-8"))
        except ValueError:
            print("Usage: exec <index|all> <command>")

    def send_script(self, target: str, local_file: str) -> None:
        """Uploads a local file to a peer and triggers its execution."""
        if not os.path.isfile(local_file):
            print(f"[ERROR] File not found: {local_file}")
            return

        with open(local_file, "rb") as f:
            file_data = f.read()

        header = f"UPLOAD:command.sh:{len(file_data)}\n".encode("utf-8")

        with self.peers_lock:
            peer_list = list(self.peers.items())

        if target.lower() == "all":
            print(f"[SEND_SCRIPT] Uploading to all peers...")
            for addr, sock in peer_list:
                try:
                    sock.sendall(header + file_data)
                except OSError:
                    self._remove_peer(addr)
            time.sleep(1.2) # Wait for network stabilization
            self._send_to_all("EXEC:all:sh /tmp/command.sh")
            return

        try:
            idx = int(target) - 1
            if idx < 0 or idx >= len(peer_list):
                print(f"[ERROR] Invalid peer index.")
                return
            addr, sock = peer_list[idx]
            print(f"[SEND_SCRIPT] Uploading to peer {idx+1}...")
            sock.sendall(header + file_data)
            time.sleep(1.2)
            sock.sendall("EXEC:all:sh /tmp/command.sh".encode("utf-8"))
        except ValueError:
            print("Usage: send_script <index|all> <local_file>")

    def status(self, target: str) -> None:
        """Quickly gathers system info from the target peer(s)."""
        status_cmd = "echo '=== SYSTEM STATUS ===' && hostname && whoami && uname -a && uptime && free -h | head -n 2 && df -h / | tail -1"
        if target.lower() == "all":
            self._send_to_all(f"EXEC:all:{status_cmd}")
        else:
            self.exec_on_peer(target, status_cmd)

    def list_peers(self) -> None:
        """Displays all currently connected nodes."""
        with self.peers_lock:
            if not self.peers:
                print("[INFO] No peers connected.")
                return
            print(f"[INFO] Connected Peers ({len(self.peers)}):")
            for i, (ip, port) in enumerate(self.peers.keys(), 1):
                print(f"  {i}. {ip}:{port}")

    def _remove_peer(self, peer_address: tuple[str, int]) -> None:
        with self.peers_lock:
            self.peers.pop(peer_address, None)
        print(f"[INFO] Peer {peer_address[0]}:{peer_address[1]} removed.")

    def shutdown(self) -> None:
        """Closes all connections and stops the server."""
        self.running = False
        with self.peers_lock:
            for sock in self.peers.values():
                try:
                    sock.close()
                except:
                    pass
            self.peers.clear()
        if self.server_socket:
            self.server_socket.close()
        print("[INFO] Node shutdown complete.")


# ========================== COMMAND LINE INTERFACE ==========================
def cli_loop(node: P2PNode) -> None:
    help_text = (
        "\nAvailable Commands:\n"
        "  connect <ip> <port>       - Connect to a new node\n"
        "  send <message>            - Broadcast text to all peers\n"
        "  exec <idx|all> <cmd>      - Execute remote shell command\n"
        "  send_script <idx|all> <f> - Upload and run local script\n"
        "  status <idx|all>          - Get system status info\n"
        "  list                      - Show active connections\n"
        "  exit                      - Close node\n"
    )
    print(help_text)

    while True:
        try:
            line = input("> ").strip()
            if not line:
                continue

            parts = line.split(maxsplit=2)
            cmd = parts[0].lower()

            if cmd == "connect":
                if len(parts) != 3: 
                    print("Usage: connect <ip> <port>")
                    continue
                node.connect_to_peer(parts[1], int(parts[2]))

            elif cmd == "send":
                if len(parts) < 2: continue
                node._send_to_all(" ".join(parts[1:]))

            elif cmd == "exec":
                if len(parts) < 3: 
                    print("Usage: exec <index|all> <command>")
                    continue
                node.exec_on_peer(parts[1], " ".join(parts[2:]))

            elif cmd == "send_script":
                if len(parts) < 3: 
                    print("Usage: send_script <index|all> <file_path>")
                    continue
                node.send_script(parts[1], parts[2])

            elif cmd == "status":
                if len(parts) < 2: 
                    print("Usage: status <index|all>")
                    continue
                node.status(parts[1])

            elif cmd == "list":
                node.list_peers()

            elif cmd in ("exit", "quit"):
                break

            elif cmd == "help":
                print(help_text)
            else:
                print(f"Unknown command: {cmd}")

        except Exception as e:
            print(f"[ERROR] {e}")

    node.shutdown()

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <port>")
        sys.exit(1)

    try:
        port = int(sys.argv[1])
    except ValueError:
        print("Invalid port number")
        sys.exit(1)

    node = P2PNode(port)
    node.start()

    try:
        cli_loop(node)
    except KeyboardInterrupt:
        print("\n[*] Interrupted by user")
    finally:
        node.shutdown()

if __name__ == "__main__":
    main()
