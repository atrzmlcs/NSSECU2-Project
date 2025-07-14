import os
import sys
from cryptography.fernet import Fernet
from datetime import datetime

# warning message
print("""\033[92m
RANSOMWARE SIMULATOR RECOVERY TOOL
This will decrypt files encrypted by encrypt.py
\033[0m""")

# user-specified directory
target_dir = sys.argv[1] if len(sys.argv) > 1 else '.'

# for logging
LOG_FILE = "ransom_simulator.log"
with open(LOG_FILE, "a") as log:
    log.write(f"\n\n--- Decryption started {datetime.now()} ---\n")


secretphrase = "password"  # change to whatever you want
user_phrase = input("Enter the secret key to decrypt files\n")

if user_phrase != secretphrase:
    print("Wrong. Retry.")
    sys.exit(1)

# encryption/decryption key
try:
    with open("Goddid.key", "rb") as key:
        secretkey = key.read()
except FileNotFoundError:
    print("ERROR: Goddid.key not found in current directory!")
    with open(LOG_FILE, "a") as log:
        log.write("ERROR: Missing Goddid.key file\n")
    sys.exit(1)

# finds encrypted files
files = []
for root, _, filenames in os.walk(target_dir):
    for file in filenames:
        filepath = os.path.join(root, file)
        if not file.endswith(".locked"):
            continue
        if file in {"sin.py", "Goddid.key", "decrypt.py", LOG_FILE}:
            continue
        files.append(filepath)
        with open(LOG_FILE, "a") as log:
            log.write(f"Found encrypted file: {filepath}\n")

# decryption logic
for filepath in files:
    try:
        
        with open(filepath, "rb") as thefile:
            contents = thefile.read()
        contents_decrypted = Fernet(secretkey).decrypt(contents)
        with open(filepath, "wb") as thefile:
            thefile.write(contents_decrypted)

        # restore original filename
        original_name = filepath.rsplit(".locked", 1)[0]
        os.rename(filepath, original_name)
        
        # logging
        print(f"Decrypted: {filepath} -> {original_name}")
        with open(LOG_FILE, "a") as log:
            log.write(f"Decrypted: {filepath} -> {original_name}\n")
    except Exception as e:
        print(f"Error processing {filepath}: {str(e)}")
        with open(LOG_FILE, "a") as log:
            log.write(f"ERROR with {filepath}: {str(e)}\n")


try:
    os.remove("README_RANSOM.txt")
    print("Removed ransom note")
except FileNotFoundError:
    pass

print(f"\nDecryption complete! {len(files)} files restored.")
