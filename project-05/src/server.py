import socket
import sys

def run_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 1337))
    s.listen(1)
    print("Server listening on 1337...")
    while True:
        try:
            conn, addr = s.accept()
            print(f"Connection from {addr}")
            data = conn.recv(1024)
            print(f"Received data: {data}")
            
            if b"GIMME_FLAG" in data:
                print("FLAG TRIGGERED")
                conn.send(b"CTF{REASSEMBLY_MASTER_8821}\n")
            else:
                conn.send(b"Access Denied. I saw: " + data + b"\n")
            conn.close()
        except Exception as e:
            print(e)

if __name__ == "__main__":
    run_server()