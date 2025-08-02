import os
import sys
from cryptography.fernet import Fernet, InvalidToken 
from datetime import datetime

#uses InvalidToken error handling for extra security measure
# Prints this message and involve user confirmation before running the encryption code. 
print("""\033[92m
RANSOMWARE SIMULATOR RECOVERY TOOL
This will decrypt files encrypted by encrypt.py
\033[0m""")

# checks if you provided a target directory to decrypt, if not, it will run on the current directory
target_dir = sys.argv[1] if len(sys.argv) > 1 else '.'

# creates/opens log file in append mode and writes a timestamp header, doesn't overwrite previous logs 
LOG_FILE = "ransom_simulator.log"
with open(LOG_FILE, "a") as log:
    log.write(f"\n\n--- Decryption started {datetime.now()} ---\n")

# hardcodes a passphrase in order to start decrypting files, exits on failure to prevent brute force attacks
secretphrase = "password"
user_phrase = input("Enter the secret key to decrypt files\n")
if user_phrase != secretphrase:
    print("Wrong. Retry.")
    sys.exit(1)

# opens the decryption key file in the target folder, and "reads" (copies) the key to the RAM
try:
    with open(os.path.join(target_dir, "secret.key"), "rb") as key:
        secretkey = key.read()
except FileNotFoundError:
    print(f"ERROR: secret.key not found in {target_dir}!")
    with open(LOG_FILE, "a") as log:
        log.write("ERROR: Missing secret.key file\n")
    sys.exit(1)

# os.walk scans the target directory and all its subfolders. will only decrypt .locked files. will skip all other files
files = [] 
for root, _, filenames in os.walk(target_dir):
    for file in filenames:
        filepath = os.path.join(root, file)
        if not file.endswith(".locked"):
            continue
        if file in {"encrypt.py", "secret.key", "decrypt.py", LOG_FILE}:
            continue
        files.append(filepath)
        with open(LOG_FILE, "a") as log:
            log.write(f"Found encrypted file: {filepath}\n")


#reads the encrypted file in read binary mode, decrypts it using secret.key, removes the .locked to restore original filename (checks if original file exists), writes decrypted data back to the file and deletes the .locked file
for filepath in files:
    try:
        # read encrypted file
        with open(filepath, "rb") as thefile:
            encrypted_data = thefile.read()
        
        # decrypt
        decrypted_data = Fernet(secretkey).decrypt(encrypted_data)
        
        # get original filename
        original_name = filepath[:-7] if filepath.endswith(".locked") else filepath
            
        # check if original file exists
        if os.path.exists(original_name):
            choice = input(f"WARNING: {original_name} exists! Overwrite? (y/n): ")
            if choice.lower() != 'y':
                continue
                
        # write decrypted data to file
        with open(original_name, "wb") as outfile:
            outfile.write(decrypted_data)
            
        # remove encrypted file
        os.remove(filepath)
        
        print(f"Restored: {filepath} -> {original_name}")
       
        
    except InvalidToken:
        print(f"Invalid token (wrong key?): {filepath}")
       
    except Exception as e:
        print(f"Error with {filepath}: {str(e)}")
       

