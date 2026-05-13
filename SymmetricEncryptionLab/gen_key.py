# gen_key.py
from cryptography.fernet import Fernet

# Open (or create) a file named 'key.txt' in 'wb' mode (write binary)
with open ('key.txt', 'wb') as f:
    # Generate a secure, random Fernet key and write it to the file
    # Fernet keys are URL-safe base64-encoded 32-byte keys
    f.write (Fernet.generate_key())
