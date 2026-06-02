import pandas as pd
import datetime
import collections
import hashlib

FILE_PATH = 'flows.csv'
INFECTED_IP = '10.1.5.97'
C2_IP = '198.51.100.202'
FLAG_FILE = 'flag.txt'

try:
    df = pd.read_csv(FILE_PATH)
except FileNotFoundError:
    print(f"Error: File '{FILE_PATH}' not found. Ensure the file is in the same directory.")
    exit()

beacon_flows = df[
    (df['src_ip'] == INFECTED_IP) &
    (df['dst_ip'] == C2_IP)
]

sel = beacon_flows['timestamp'].tolist()

if not sel:
    print(f"Error: No beaconing flows found between {INFECTED_IP} and {C2_IP}.")
    exit()

print(f"Total identified beaconing flows: {len(sel)}")

gaps = []
for a, b in zip(sel, sel[1:]):
    ta = datetime.datetime.fromisoformat(a)
    tb = datetime.datetime.fromisoformat(b)
    gaps.append((tb - ta).total_seconds())

half = gaps[:max(10, len(gaps) // 2)]
rounded = [int(round(x)) for x in half if x > 20]
mode_counter = collections.Counter(rounded)

if mode_counter:
    mode = mode_counter.most_common(1)[0][0]
else:
    mode = 0

period_seconds = mode
domain = "c2.evil-domain.example"
hostname = "WIN-PC-07"

final_string = f"{domain}|{period_seconds}|{hostname}"

sha256_hash = hashlib.sha256(final_string.encode('utf-8')).hexdigest()

try:
    with open(FLAG_FILE, 'w') as f:
        f.write(sha256_hash + '\n')
    
    print("-" * 40)
    print(f"Rounded time gaps list: {rounded}")
    print(f"Final Beacon Period: {mode} seconds")
    print("-" * 40)
    print(f"Input string for SHA256: {final_string}")
    print(f"SHA256 Result: {sha256_hash}")
    print(f"\nFinal hash successfully saved to '{FLAG_FILE}'.")

except Exception as e:
    print(f"Error writing to file: {e}")
