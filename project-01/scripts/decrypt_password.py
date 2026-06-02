import base64
import urllib.parse
import os 

encoded_data = "MjYqIR4kO1QwOjokJCse"
xor_key = "secret"

try:
    decoded_url = urllib.parse.unquote(encoded_data)
    xor_bytes = base64.b64decode(decoded_url)
except Exception as e:
    print(f"Error during Base64 decoding: {e}")
    xor_bytes = base64.b64decode(encoded_data)

def xor_decrypt(data_bytes, key):
    """
    Performs repeating-key XOR decryption on the data bytes.
    """
    key_bytes = key.encode('utf-8')
    decrypted_bytes = bytearray()
    key_len = len(key_bytes)
    
    for i in range(len(data_bytes)):
        decrypted_byte = data_bytes[i] ^ key_bytes[i % key_len]
        decrypted_bytes.append(decrypted_byte)
    return decrypted_bytes.decode('utf-8')

flag = xor_decrypt(xor_bytes, xor_key)

print("--- Final Result ---")
print(f"Encrypted String (p7wd): {encoded_data}")
print(f"Base64 Decoded to XORed Bytes: {xor_bytes}")
print(f"XOR Key Used: {xor_key}")
print(f"Original Password (FLAG): {flag}")

try:
    with open("flag.txt", "w") as f:
        f.write(flag + "\n")
    print("\n[+] Successfully wrote FLAG to flag.txt")
except Exception as file_error:
    print(f"\n[!] Error writing to file: {file_error}")
