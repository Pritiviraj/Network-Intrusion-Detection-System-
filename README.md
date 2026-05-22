# Network Intrusion Detection System (NIDS)

A real-time Network Intrusion Detection System that monitors live network traffic, detects cyber attacks, automatically blocks malicious IPs, and displays alerts on a live dashboard.

## Features

- Real-time traffic monitoring with Suricata IDS
- 10 custom detection rules (port scans, SQL injection, SSH brute force, ping floods, XSS, and more)
- 45,000+ community detection rules from Emerging Threats
- Automatic IP blocking for critical severity attacks
- Live web dashboard with charts and alert table
- Color-coded terminal alert monitor

## Tech Stack

- Suricata 7.x (IDS engine)
- WSL 2 with Ubuntu 22.04
- Python 3 + Flask
- Chart.js for visualizations
- iptables for auto-blocking

## Project Structure

nids-project/ ├── alert_monitor.py # Watches logs and prints/block alerts ├── app.py # Flask web server ├── dashboard_data.py # Parses logs for dashboard ├── templates/ │ └── dashboard.html # Live dashboard UI └── response_log.txt # Log of blocked IPs

## Installation

Follow the step-by-step guide in NIDS_Setup_Guide.html. Key commands: sudo add-apt-repository ppa:oisf/suricata-stable -y && sudo apt update && sudo apt install suricata -y && pip3 install flask watchdog pandas --break-system-packages && sudo pip3 install suricata-update --break-system-packages && sudo suricata-update

## Running the System

Open three Ubuntu terminals. Terminal 1 (Suricata): sudo suricata -c /etc/suricata/suricata.yaml -i eth0. Terminal 2 (Monitor): cd ~/nids-project && python3 alert_monitor.py. Terminal 3 (Dashboard): cd ~/nids-project && python3 app.py. Then open browser to http://localhost:5000

## Detection Rules (10 Custom Rules)

SID 1000001: ICMP Ping Flood (10 packets / 5 seconds). SID 1000002: TCP Port Scan (20 SYNs / 10 seconds). SID 1000003: SSH Brute Force (5 attempts / 60 seconds). SID 1000004: SQL Injection (OR 1=1). SID 1000005: SQL Injection (UNION SELECT). SID 1000006: Telnet Attempt (port 23). SID 1000007: FTP Brute Force (5 attempts / 30 seconds). SID 1000008: Directory Traversal (../ pattern). SID 1000009: XSS Attempt (<script> tag). SID 1000010: RDP Brute Force (5 attempts / 60 seconds).

## Testing the System

Run from 4th terminal: ping -c 50 -i 0.05 127.0.0.1 && sudo nmap -sS -p 1-1000 127.0.0.1 && curl "http://127.0.0.1/login?u=%27%20OR%20%271%27%3D%271"

## Common Issues & Fixes

suricata: command not found -> sudo apt install suricata -y. WSL version 1 -> wsl --set-version Ubuntu-22.04 2. Permission denied on eve.json -> sudo chmod 644 /var/log/suricata/eve.json. Flask port in use -> kill $(lsof -t -i:5000). TemplateNotFound error -> Run Flask from ~/nids-project.

## Screenshots for Submission

suricata --version output, Terminal 1 showing all engines started, Terminal 2 showing colored alerts, Dashboard with populated charts, VS Code showing local.rules, Project file structure, fast.log content, suricata-update output

## Task Completion

Set up NIDS environment: Complete. Configure rules and alerts: Complete. Monitor network traffic: Complete. Implement response mechanisms: Complete. Visualize detected attacks: Complete.

## Author

Cybersecurity Internship Project

## License

Educational Use Only