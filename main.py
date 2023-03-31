import json
from charm.toolbox.pairinggroup import PairingGroup, GT
from CPabe09 import CPabe09
from utils import grp_to_str, encrypt_file, decrypt_file, serialize_dict_elements, deserialize_dict_elements
from constants import *

# Define users and attributes

users = {
    # "Soham": ['THREE', 'ONE', 'TWO'],
    # "Silambararan": ['TWO', 'FOUR']
    # "John": ["FINANCE", "SENIOR"],
    "Sarah": ["HR", "MANAGER"],
    # "Peter": ["FINANCE", "JUNIOR"],
    # "Lisa": ["FINANCE", "MANAGER"],
    # "Rachel": ["HR", "SENIOR"],
    # "Alex": ["SALES", "SENIOR"],
}


def decrypt_and_store_file(name, attributes, file_path, encrypted_key_message_deserialized, cpabe, master_public_key,
                           master_private_key):
    print("Name = ", name, " | Attributes = ", attributes)

    user_key = cpabe.keygen(master_public_key, master_private_key, attributes)

    decrypted_message = cpabe.decrypt(master_public_key, user_key, encrypted_key_message_deserialized)

    if decrypted_message:
        print("Decryption Successful")
        key_str = grp_to_str(decrypted_message)
        print(key_str)
        decrypt_file(file_path, key_str)
        # print("Decrypted message  = ", decrypted_message)
    else:
        print("Decryption Unsuccessful ❌")


def encrypt_and_store_file_key(groupObj, file_path, cpabe, master_public_key, policy):
    # Using random element from the GT group to encrypt the file using AES
    message = groupObj.random(GT)
    key_str = grp_to_str(message)
    encrypt_file(file_path, key_str)
    print("AES Key = ", message)

    # Encrypting the key and storing it in file
    encrypted_key_message = cpabe.encrypt(master_public_key, message, policy)
    print("encrypted_key_message = ", encrypted_key_message)
    encrypted_key_message_serialised = encrypted_key_message.copy()
    serialize_dict_elements(encrypted_key_message_serialised, groupObj)
    print(encrypted_key_message_serialised)
    with open('keys/element_dict.json', 'w') as f:
        json.dump(encrypted_key_message_serialised, f)


def main():
    file_path = "files/numbers.txt"

    # Define Policy
    policy = '(((FINANCE and (SENIOR or MANAGER)) or (HR and MANAGER)))'
    print("Policy = ", policy)

    # Initializing CPABE System
    groupObj = PairingGroup('SS512')  # Get the elliptic curve with the bilinear mapping feature needed.
    cpabe = CPabe09(groupObj)
    (master_private_key, master_public_key) = cpabe.setup(g1=g1, g2=g2, alpha=alpha, a=a)
    # (g1, g2, alpha, a) = cpabe.setup()
    # print(groupObj.serialize(g1))
    # print(groupObj.serialize(g2))
    # print(groupObj.serialize(alpha))
    # print(groupObj.serialize(a))
    print("Master Public key = ", master_public_key)
    print("Master Private key = ", master_private_key)

    print("Select a choice : ")
    while True:

        print("1] Encrypt a file")
        print("2] Decrypt a file")
        num_str = input("Enter your choice: ")
        choice = int(num_str)

        if choice == 1:
            encrypt_and_store_file_key(groupObj, file_path, cpabe, master_public_key, policy)

        elif choice == 2:
            name = input("Enter name : ")
            print("Enter the attributes : (Enter 'x' to stop)")
            attributes = []
            while True:
                response = input()
                if response == "x":
                    break
                attributes.append(response)

            with open('keys/element_dict.json', 'r') as f:
                encrypted_key = json.load(f)

            deserialize_dict_elements(encrypted_key, groupObj)
            print("encrypted_key_message_deserialized = ", encrypted_key)
            decrypt_and_store_file(name, attributes, file_path, encrypted_key, cpabe, master_public_key, master_private_key)


if __name__ == "__main__":
    main()
