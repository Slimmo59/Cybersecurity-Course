# decript.py
from cryptography.fernet import Fernet
import os

def decrypt_files_in_directory(directory, key_file):
    """
    Scans a directory and attempts to decrypt all files using the provided key.
    """
    targets = []

    # 1. Retrieve the list of files to decrypt in the specified directory
    for _, _, f in os.walk(directory):
        targets.extend(f)
    print("Files to decrypt:", targets)

    # 2. Load the symmetric encryption key from the key file
    # This must be the exact same key used during encryption
    with open(key_file, 'rb') as file:
        key = file.read()

    # Initialize the Fernet cipher suite with the loaded key
    cipher_suite = Fernet(key)

    # 3. Restoration process
    for target in targets:
        file_path = f'{directory}/{target}'
        
        # Read the encrypted binary content
        with open(file_path, 'rb') as fil:
            encrypted_content = fil.read()
            
        try:
            # Attempt to decrypt the content
            decrypted_content = cipher_suite.decrypt(encrypted_content)

            # Overwrite the file with the original decrypted data
            with open(file_path, 'wb') as file_:
                file_.write(decrypted_content)
            print(f"[OK] Decrypted: {target}")
            
        except Exception as e:
            # Fernet raises an error if the key is incorrect or the file is not encrypted/corrupted
            print(f"[ERROR] Failed to decrypt {target}: Invalid key or corrupted file.")

if __name__ == "__main__":
    # Default settings for target directory and key file
    target_directory = 'targets'
    key_path = 'key.txt'
    
    # Run the decryption process
    decrypt_files_in_directory(target_directory, key_path)
