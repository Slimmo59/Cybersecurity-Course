import socket

# The IP address of the server (e.g., your Kali Linux machine)
ip = "192.168....." 
port = 4444

def main():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = (ip, port)
    
    try:
        # Connect the socket to the server's address and port
        sock.connect(address)
        
        # Receive data from the server (up to 1024 bytes)
        msg = sock.recv(1024)
        
        # Decode the received bytes back into a string and print it
        print("Message received:")
        print(msg.decode())
        
    except ConnectionRefusedError:
        print("Error: Could not connect to the server. Is it running?")
    finally:
        # Ensure the socket is closed after the operation
        sock.close()

if __name__ == "__main__":
    main()
