import base64

from Crypto.Cipher import AES
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from charm.toolbox.pairinggroup import PairingGroup


def encrypt_file(file_path, key):
    nonce = get_random_bytes(16)

    # Create the AES cipher
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)

    # Read the entire file into memory
    with open(file_path, "rb") as f:
        data = f.read()

    # Encrypt the data
    ciphertext, tag = cipher.encrypt_and_digest(data)

    # Write the encrypted data and tag to the output file
    with open(file_path, "wb") as f:
        f.write(nonce)
        f.write(ciphertext)
        f.write(tag)


def decrypt_file(file_path, key):
    print(file_path)
    # start_time = datetime.datetime.now()
    # Read the nonce, ciphertext, and tag from the encrypted file
    with open(file_path, 'rb') as file:
        nonce = file.read(16)
        ciphertext = file.read()
        tag = ciphertext[-16:]
        ciphertext = ciphertext[:-16]

    # Create the AES cipher object
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)

    # Decrypt the ciphertext and verify the authentication tag
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)

    # Write the decrypted data to the output file
    with open(file_path, 'wb') as file:
        file.write(plaintext)


def serialize_dict_elements(dic, group):
    for key, value in dic.items():
        if type(value) == dict:
            serialize_dict_elements(value, group)
        elif type(value) == str:
            return
        else:
            dic[key] = base64.b64encode(group.serialize(value)).decode('utf-8')


def deserialize_dict_elements(dic, group):
    for key, value in dic.items():
        if type(value) == dict:
            deserialize_dict_elements(value, group)
        # elif type(value) == str:
        #     return
        else:
            try:
                dic[key] = group.deserialize(base64.b64decode(value.encode(
                    'utf-8')))  # groupObj.deserialize(value.encode('utf-8')) #groupObj.deserialize(value).encode('utf-8')
            except:
                pass


def grp_to_str(element):
    """
    Convert the element from the curve to 32 byte AES key
    :param element: element from the elliptical curve
    :return: AES key
    """
    group = PairingGroup('SS512')

    # Convert the element to a byte string
    g_bytes = group.serialize(element)

    return g_bytes[:32]
