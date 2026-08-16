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

### Latest Release: v2.0.1

The official release package is available for testing:

* **Download:** [Sentinel_V2 v2.0.1 Release Package](https://github.com/Fikashongwe/Sentinel_V2/releases/tag/v2.0.1)
* **Contents:**
  * `sentinel_v2.exe` — Standalone compiled Windows executable.
  * `Sentinel_Shield_Beta_Release.zip` — Compressed distribution package.

---

---

## 🚀 Getting Setup

### Dependencies
```bash
pip install psutil wmi pywin32 requests urllib3
# Compilation
python -m PyInstaller SentinelV2.spec
