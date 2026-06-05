# Challange: Silent Jammer (Selective Jamming)

## Overview
This project focuses on a **selective jamming** challenge in a wireless communication setting.  
A sender transmits frames, and the receiver sends an ACK when a frame is received correctly. The goal is to **jam only the ACK at the right time** so that the transmission is disrupted without triggering detection. If jamming is too aggressive, the receiver detects the interference and the attack fails.

## Challenge Goal
The objective of this challenge is to:
- understand the frame/ACK exchange,
- identify the correct timing for selective jamming,
- implement the jamming logic in the provided solution script,
- and make the receiver print the flag.

## Repository Structure
```text
project-05/
├── README.md
├── src/
└── scripts/
```
## Project Workflow
   - Start the environment with:
```text
   docker compose up --build 
```
   
   - Study the communication flow between sender and receiver.
   - Implement the selective jamming logic in solve_jam.py.
   - Jam only the ACK at the correct moment.
   - Avoid over-jamming so the receiver does not detect interference.
   - Trigger the condition that makes the receiver print the flag.
## Key Idea
The challenge is based on timing-sensitive wireless jamming:

   - the sender transmits frames,
   - the receiver responds with ACKs,
   - only the ACK should be jammed,
   - excessive interference causes detection.
     
This makes the challenge a good exercise in precise link-layer attack timing and controlled disruption.

## Deliverable
The expected result is the exact flag printed by the receiver.
