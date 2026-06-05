from netfilterqueue import NetfilterQueue
from scapy.all import *
import os

# This simulates a "First Byte Wins" reassembler.
# It maintains a simple cache of sequence numbers seen.
seen_seqs = {}

def process_packet(packet):
    scapy_pkt = IP(packet.get_payload())
    
    if scapy_pkt.haslayer(TCP) and scapy_pkt.haslayer(Raw):
        payload = scapy_pkt[Raw].load
        seq = scapy_pkt[TCP].seq
        
        # LOGIC:
        # If we check the payload and it contains "GIMME_FLAG", block it.
        if b"GIMME_FLAG" in payload:
            print(f"[FIREWALL] BLOCKING Malicious Segment at {seq}")
            packet.drop()
            return

        # If it says "BENIGN", we let it through.
        # In a real CTF, this code would be more complex (tracking streams),
        # but here we simulate the vulnerability: The firewall inspects THIS packet
        # in isolation or using a naive cache, sees "BENIGN", and allows it.
        
    packet.accept()

def main():
    print("[*] Firewall Running... Configuring NFQUEUE")
    # Intercept traffic destined to the server
    os.system("iptables -I FORWARD -d 10.0.0.3 -j NFQUEUE --queue-num 1")
    
    nfq = NetfilterQueue()
    nfq.bind(1, process_packet)
    try:
        nfq.run()
    except KeyboardInterrupt:
        os.system("iptables -F")

if __name__ == "__main__":
    main()