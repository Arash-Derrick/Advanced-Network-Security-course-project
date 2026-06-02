import base64

def decode_base64_with_auto_padding():
    print("--- decode_base64 ---")
    encoded_input = input("enter sting of base64 for decoding: ").strip()
    if not encoded_input:
        print("error: your input is empty")
        return
    original_length = len(encoded_input)
    padding_needed = (4 - (original_length % 4)) % 4
    padded_input = encoded_input + ('=' * padding_needed)
    print("-" * 40)
    print(f"original_length: {original_length}")
    print(f"number of '=' added: {padding_needed}")
    print(f"string with modified padding: {padded_input}")
    print("-" * 40)
    try:
        decoded_bytes = base64.b64decode(padded_input.encode('ascii'))
        decoded_string = decoded_bytes.decode('utf-8')
        print(f"✅ decoded string: {decoded_string}")
    except Exception as e:
        print(f"❌ error decoded (invalid Base64): {e}")
decode_base64_with_auto_padding()
