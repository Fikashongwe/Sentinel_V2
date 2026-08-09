# Sentinel_V2

## Overview
Sentinel_V2 is an automated, multi-sensor Endpoint Detection and Response (EDR) and behavioral threat isolation framework built in Python. Designed for modern Linux and Windows environments, it provides real-time visibility and rapid mitigation against ransomware, file tampering, and unauthorized privilege escalation.

## Core Architecture
- **Entropy Sensor:** Computes Shannon entropy over target directories to detect rapid, unapproved file encryptions.
- **File Integrity Monitor (FIM):** Audits file system events and alerts on unauthorized modifications or deletions.
- **Automated Response Engine:** Executes granular process/network isolation actions upon trigger conditions.
- **SecOps Telemetry:** Integrates directly with Slack webhooks to stream live incident notifications into dedicated operational channels.

## Tech Stack
- **Language:** Python
- **Environment:** Ubuntu Linux / Windows 11
- **Alerting:** Slack API Webhooks
