# Network Intrusion Detection System (NIDS)

A real-time Network Intrusion Detection System that monitors live network traffic, detects malicious activity using Suricata IDS, auto-blocks attacking IPs, and visualizes alerts through a live Flask dashboard.

## Features

- **Real-time traffic monitoring** using Suricata IDS engine
- **10+ custom detection rules** (ping flood, port scans, SQL injection, SSH/FTP/RDP brute force, XSS, directory traversal)
- **45,000+ community rules** from Emerging Threats Open
- **Automatic IP blocking** for critical severity attacks using iptables
- **Live web dashboard** with:
  - Alert count statistics
  - Top attack signatures (bar chart)
  - Alerts by category (doughnut chart)
  - Recent alerts table with severity coloring
  - Auto-refresh every 30 seconds
- **Color-coded terminal alert monitor** with real-time output

## Tech Stack

| Component | Technology |
|-----------|------------|
| IDS Engine | Suricata 7.x |
| Platform | WSL 2 (Ubuntu 22.04 on Windows) |
| Backend | Python 3, Flask |
| Log Monitoring | Watchdog (file system events) |
| Dashboard | HTML5, Chart.js, CSS3 |
| Attack Simulation | Nmap, hping3, cURL |

## Project Structure
