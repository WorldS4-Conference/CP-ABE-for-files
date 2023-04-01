import base64

# Convert the byte string to a 32-character string using base64 encoding
original_string = b'3:b1+M25Szw3uwqibrlrfTC6XLoR1F2RNH7AoNonb9qm5fMLOnix6NBznLsvLUrbryvBUP0qgI7JhgJBOUVENkrWx6wzMuK4+vxMOaYdAFggBnEte8iUeRfaM8s0ne6UUxfESndqyTx5YYvj2YzIPTvu9uMWYlItVw7A/H2O1JnZw='
encoded_string = base64.b64encode(original_string)
print("encoded_string = ", encoded_string)

encoded_string_32 = encoded_string[:32].decode('utf-8')
print("encoded_string_32 = ", encoded_string_32)


# # Convert the 32-character string back to the original byte string using base64 decoding
# decoded_string = base64.b64decode(encoded_string_32 + '==' + encoded_string[32:].decode('utf-8'))
# print("decoded_string = ", decoded_string)
#
# print(original_string == decoded_string)

