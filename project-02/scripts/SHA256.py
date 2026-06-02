import hashlib

root_name = "WINWORD.EXE"
root_pid = "2310"
timestamp_utc = "2025-10-26T12:27" 

flag_string = f"{root_name}|{root_pid}|{timestamp_utc}"

sha256_digest = hashlib.sha256(flag_string.encode('utf-8')).hexdigest()

print(f"Input String: {flag_string}")
print(f"SHA256 Hash: {sha256_digest}")


try:
    with open("flag.txt", "w") as f:
        f.write(sha256_digest + "\n")
    print(f"\n[+] Hash successfully written to flag.txt")
except Exception as e:
    print(f"\n[!] Error writing to file: {e}")
