import os
from cryptography.fernet import Fernet


files = []

for file in os.listdir():
        if not file.endswith(".locked"):
                continue
        if file in {"sin.py", "Goddid.key", "decrypt.py"}:
                continue
        files.append(file)

print(files)

with open("Goddid.key", "rb") as key:
                secretkey=key.read()

secretphrase = "password" #change to whatever u want

user_phrase = input("Enter the secret key to decrypt files\n")
if user_phrase == secretphrase:
        for file in files:
                with open(file, "rb") as thefile:
                        contents =  thefile.read()
                contents_decrypted = Fernet(secretkey).decrypt(contents)
                with open(file, "wb") as thefile:
                        thefile.write(contents_decrypted)

                original_name, _ = os.path.splitext(file)
                os.rename(file, original_name)
                print(f"Decrypted and renamed to: {file} -> {original_name}") #reverts back .locked to normal file

        print("Your files have been decrypted.")
else:
        print("Wrong. Retry.")
