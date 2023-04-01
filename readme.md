
# CP-ABE File Encryption and Decryption using Python

This project is a Python implementation of CP-ABE (Ciphertext-Policy Attribute-Based Encryption) for file encryption and decryption. It uses the Charm Crypto library for implementing the CP-ABE scheme and the PyCryptodome library for AES encryption.

This is a Python project that uses CP-ABE (ciphertext-policy attribute-based encryption) to encrypt and decrypt files. The implementation uses Charm Crypto, a Python library for secure and efficient cryptography, and the PyCryptodome library for AES encryption and decryption.

### main.py
main.py is the main driver file for the project. It provides an interface for encrypting and decrypting files using CP-ABE. The file contains the logic for generating keys, encrypting and decrypting files, and serializing and deserializing objects.

### utils.py
This module contains several utility functions used in the project. 

### constants.py
The variables g1, g2, alpha, and a are parameters used in the CP-ABE system. They represent elements of mathematical groups used in the encryption and decryption process. They are represented as byte strings

### CPabe09.py
This is a Python implementation of the Ciphertext-Policy Attribute-Based Encryption (CP-ABE) scheme proposed by Bethencourt, Sahai, and Waters in their 2009 paper "Ciphertext-Policy Attribute-Based Encryption".

The setup function is modified. It takes four parameters - g1, g2, alpha, and a. If all four parameters are not None i..e they are provided, then the function deserializes them using the Charm library's deserialize method. Otherwise, it generates random values for g1, g2, alpha, and a. 

### /keys
Folder for storing the keys of files

### /files
Folder for storing the files in encrypted or decrypted form

### make_sample_file.py
This generate a sameple file of size 2MB containing 1's which can be used for testing purpose.


## Usage

***The policy and file path is hardcoded os of now***

Run the main.py and follow the console log

