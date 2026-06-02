# Phishing Post-Mortem Analysis

This subproject presents a forensic reconstruction of a phishing attack. By analyzing the phishing email, client-side JavaScript, access logs, and developed solution scripts, the attack chain was reversed to recover the exfiltrated credentials.

## Overview
The objective of this exercise was to investigate a phishing campaign that utilized dynamic parameters, obfuscated form-field generation, and layered encoding to conceal stolen payloads.

The attack flow was reconstructed as follows:
1. **Parameter Extraction**: Analyzing the malicious URL for tracking tokens.
2. **Reverse Engineering**: Deconstructing client-side logic used for dynamic field naming.
3. **Log Correlation**: Mapping victim activity within web access logs.
4. **Payload Decryption**: Reversing the encoding pipeline to recover the original data.

## Repository Structure
```text
project-01/
├── README.md
├── src/
│   ├── landing.html
│   ├── landing.js
│   ├── mail.eml
│   └── web_access.log
└── scripts/
├── decode-Base64.py
└── decrypt_password.py
Technical Analysis
1) Phishing URL and Campaign Tracking
The phishing URL utilized dynamic parameters to identify targets:

cid=Q2FtcGFpZ25JRD0xMjM (Decodes to CampaignID=123)
n=nonce-7f
These parameters were used to personalize the landing page and track the success rate of the campaign.

2) Client-Side Field Obfuscation
The landing.js file dynamically generated form field names based on the session’s nonce. For instance, the script derived keys like ufsr and p7wd instead of standard names like username or password. This technique effectively evades simple static signature-based detection.

3) Log-Based Evidence Collection
The web access logs captured a critical POST request to the attacker’s endpoint:

POST /c?t=precomputed-client

The logged payload contained:

ufsr (User Identifier)
p7wd (Obfuscated Secret)
cid (Campaign ID)
4) Payload Recovery Pipeline
The captured payload was protected using a layered transformation scheme. The recovery process, implemented in the scripts/ directory, follows these steps:

URL Decoding: Normalizing the log data.
Base64 Decoding: Converting the transport-ready string back to binary.
XOR Decryption: Applying the recovered key (secret) to reveal the plaintext.
Result
By executing the decrypt_password.py script, the layered protection was successfully stripped, leading to the full recovery of the original hidden credential (Flag).

Skills Demonstrated
Phishing Artifact Analysis: Analyzing .eml and .html files for threat intelligence.
JavaScript Reverse Engineering: Understanding dynamic obfuscation techniques.
Web Log Forensics: Isolating malicious traffic from legitimate server logs.
Cryptographic Reversal: Implementing decryption routines (XOR, Base64).
Security Automation: Using Python to automate forensic workflows.
Advanced Network Security course project.