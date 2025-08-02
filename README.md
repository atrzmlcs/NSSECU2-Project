# Ransomware Simulator

This project is a simulation of a simple ransomware-style tool intended for **educational purposes only**. It includes two Python scripts: `encrypt.py` and `decrypt.py`.

This tool is for academic demonstration only. Do not run it on files, folders, or systems you do not own or have explicit permission to simulate attacks on.

---

## Project Structure
```
project/
├── tool/
│ ├── encrypt.py
│ └── decrypt.py
└── attack/
├── file1.txt
├── image.jpg
└── report.pdf
```
- `tool/`: Contains the ransomware simulation scripts.
- `attack/`: Folder representing the victim’s environment with files to encrypt. This can contain any file.

---

## How to Use

### 1. Set Up Folders

Create two folders:

- One named `tool/` containing `encrypt.py` and `decrypt.py`
- Another named `attack/` containing test files such as `.txt`, `.jpg`, or `.pdf`

### 2. Encrypt Files

Open a terminal and navigate to the `tool/` directory:
```
cd <path/to/tool>
```
Run the encryption script with the path to the victim folder:

```
python3 encrypt.py <path/to/attack>
```

This will encrypt all files inside the specified folder.

### 3. Decrypt Files

Run the decryption script using the same path:

```
python3 decrypt.py <path/to/attack>
```

You will be prompted to enter the passphrase.

---

## Passphrase for Decryption

```
password
```

If the correct passphrase is entered, all encrypted files will be restored.

---

## Features

- Encrypts and decrypts files in a specified directory
- Simple command-line usage
- Demonstrates core ransomware behavior for educational purposes

---

## Author and Credits

This project was created by the following members:
- Aguete, Sofia Ashley
- Gaspar, Chrisane Ianna
- Leander, Wendel Walter
- Maglente, Michael Stephen
- Malicsi, Atreuz Patrick
