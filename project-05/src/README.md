# Ex1: The Ghost in the Stream (TCP reassembly mismatch)

Goal
- A “smart” middlebox firewall inspects TCP payloads and blocks the string `GIMME_FLAG`.
- The firewall and the server reassemble overlapping TCP segments differently.

Run
```bash
sudo docker compose up -d --build
```

If you hit setup issues (only if needed)
- If Docker fails with a network/subnet overlap error, reset unused Docker networks:
```bash
sudo docker network prune -f
```

Student task
- Target service: `10.123.45.3:1337`
- Write `solve.py` (or `exploit.py`) that:
  - Establishes a TCP connection
  - Sends overlapping or out-of-order TCP segments
  - Causes the server to receive `GIMME_FLAG` while the firewall does not detect it
- Capture and print the returned flag.

Notes
  - If your connection dies right after the handshake, you can temporarily drop RSTs for your chosen source port:
```bash
sudo iptables -I OUTPUT -p tcp --tcp-flags RST RST --sport 12345 -j DROP
```
  - Remove the rule after you finish:
```bash
sudo iptables -D OUTPUT -p tcp --tcp-flags RST RST --sport 12345 -j DROP
```
- Timing matters: ensure your out-of-order/overlap segments arrive within the same TCP session.