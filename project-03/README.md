# E1-C3 Challenge

This project is a network forensics challenge focused on **malicious traffic analysis** and **beacon period extraction**.  
The goal is to correlate multiple telemetry sources to identify suspicious periodic communication, map the infected host, and trace the control infrastructure.

## Overview

The investigation combines several data sources to reconstruct the behavior of the malicious traffic:

- `flows.csv`
- `dns.log`
- `dhcp_leases.csv`
- `tls_fingerprints.csv`
- `asn_map.csv`

Using these artifacts, the analysis identifies:

- periodic low-volume network flows consistent with beaconing
- the internal host involved in the activity
- the destination domain and IP
- supporting ASN / TLS evidence for infrastructure attribution

## Methodology

The workflow follows a structured correlation process:

1. **Flow analysis**
   - Inspect network flows for repeated, low-byte, periodic communication.
   - Detect timing patterns consistent with beaconing behavior.

2. **DNS correlation**
   - Use DNS logs to map suspicious destination IPs to their domain names.

3. **Host attribution**
   - Use DHCP lease records to map internal IPs to the corresponding workstation.

4. **Infrastructure validation**
   - Cross-check destination ownership with ASN mapping.
   - Use TLS fingerprint data to support the attribution.

5. **Final reconstruction**
   - Combine all evidence to extract the beacon period and reconstruct the malicious communication pattern.

## Skills Demonstrated

- Network traffic analysis
- Beaconing detection
- DNS and DHCP correlation
- ASN-based infrastructure attribution
- TLS fingerprint analysis
- Threat hunting methodology

## Repository Structure
```text
.
├── src/          # Original challenge files
├── scripts/      # Solution scripts and analysis helpers
└── README.md
```