# The Ground Truth Detective Hard Mode

This project is a digital forensics and threat-hunting exercise focused on reconstructing the **ground truth** of a suspicious incident by correlating multiple telemetry sources across the network and endpoint stack.

## Overview

The investigation centers on identifying the root process behind a suspicious communication pattern by combining evidence from:

- NetFlow
- NAT logs
- DHCP leases
- Proxy logs
- JA3 / TLS fingerprint data
- EDR event telemetry

The goal is to infer the true process metadata — including process name, PID, and creation time — and use those values to reproduce a final SHA-256 digest.

## Objective

The challenge demonstrates how independent forensic artifacts can be stitched together to answer one question:

> **Which process was truly responsible for the observed activity?**

To do that, the investigation reconstructs:

- the affected host
- the internal and external IP mappings
- the process ID
- the TLS fingerprint
- the process creation timestamp

## Methodology

The analysis follows a correlation-based workflow:

1. **Network attribution**
   - Inspect NetFlow and NAT records to trace suspicious outbound activity.
   - Use DHCP lease data to map internal IP addresses to the host identity.

2. **Proxy and TLS analysis**
   - Review proxy logs and JA3/TLS fingerprints to associate the traffic with a specific client behavior.

3. **Endpoint validation**
   - Correlate the network findings with EDR events to identify the responsible process and its PID.

4. **Ground-truth reconstruction**
   - Determine the process name, PID, and UTC creation time.
   - Normalize the timestamp to minute precision where required.

5. **Final verification**
   - Feed the recovered values into the SHA-256 generator script to produce the final digest.

## Repository Structure
```text
.
├── src/          # Original files provided by the instructor
├── scripts/      # Solution scripts and analysis helpers
└── README.md
SHA-256 Verification
The repository includes a small helper script that generates a deterministic SHA-256 hash from the recovered forensic tuple:

text
process_name | process_id | utc_creation_time
This script is used as the final verification step after the ground truth has been reconstructed from the evidence.

Skills Demonstrated
Network forensic correlation
Host attribution from DHCP/NAT artifacts
Proxy and TLS fingerprint analysis
Endpoint telemetry investigation
Process provenance reconstruction
SHA-256 based verification workflow
Notes
The repository is intentionally structured to emphasize analysis and methodology, not spoilers.
No final answer or flag is stored in the repository.
The final digest is generated only through the analysis process.
