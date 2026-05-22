# Network Intrusion Detection System (NIDS) - Complete Setup Guide

A real-time Network Intrusion Detection System that monitors live network traffic, detects cyber attacks, automatically blocks malicious IPs, and displays alerts on a live dashboard.

================================================================================

TABLE OF CONTENTS

+--------+--------------------------------+
| Phase | Title                          |
+-------+---------------------------------+
| 1     | Environment Setup              |
| 2     | Configure Suricata             |
| 3     | Detection Rules                |
| 4     | Python Files                   |
| 5     | Dashboard HTML                 |
| 6     | Launch System                  |
| 7     | Simulate Attacks               |
| 8     | Troubleshooting                |
+-------+---------------------------------+

================================================================================

PHASE 1: ENVIRONMENT SETUP

Step 1: Enable WSL on Windows
- Press Windows key, type "PowerShell", right-click and select "Run as administrator"
- Run: dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
- Run: dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
- Restart your computer: Restart-Computer

Step 2: Install Ubuntu after restart
- Open PowerShell as Administrator again
- Run: wsl --set-default-version 2
- Run: wsl --install -d Ubuntu-22.04
- When prompted, create a username (e.g., student) and password
- Verify: wsl --list --verbose (should show VERSION 2)

Step 3: Install VS Code
- Download from https://code.visualstudio.com/download
- Run installer and check "Add to PATH" during installation
- Open VS Code and install the WSL Extension by Microsoft

Step 4: Open Ubuntu and update
- Open Ubuntu from Start Menu
- Run: sudo apt update && sudo apt upgrade -y

Step 5: Install Python 3
- Run: sudo apt install python3 python3-pip python3-venv -y
- Verify: python3 --version (should show Python 3.10+)

Step 6: Install Suricata
- Run: sudo add-apt-repository ppa:oisf/suricata-stable -y
- Run: sudo apt update
- Run: sudo apt install suricata -y
- Verify: suricata --version (should show 7.x.x)

Step 7: Install Python Libraries
- Run: pip3 install flask watchdog pandas --break-system-packages
- Verify: python3 -c "import flask; print('Flask OK:', flask.__version__)"

================================================================================

PHASE 2: CONFIGURE SURICATA

Step 1: Find your network interface
- Run: ip a
- Look for eth0, ens33, or similar (not 127.0.0.1) and write this name down

Step 2: Copy and edit config
- Run: sudo cp /etc/suricata/suricata.yaml ~/suricata.yaml
- Run: code ~/suricata.yaml

Step 3: Edit HOME_NET
- In VS Code, press Ctrl+H
- Find: HOME_NET: "[192.168.0.0/16,10.0.0.0/8,172.16.0.0/12]"
- Replace with: HOME_NET: "[192.168.0.0/16,10.0.0.0/8,172.16.0.0/12,172.20.0.0/14]"
- Click Replace All

Step 4: Set network interface
- Press Ctrl+F and search for "af-packet"
- Find the line that says interface: eth0
- Change eth0 to your interface name from Step 1

Step 5: Enable EVE JSON logging
- Search for "eve-log"
- Find enabled: no and change it to enabled: yes

Step 6: Save and copy back
- Press Ctrl+S to save
- Run: sudo cp ~/suricata.yaml /etc/suricata/suricata.yaml

Step 7: Test configuration
- Run: sudo suricata -T -c /etc/suricata/suricata.yaml -v
- Expected output: "Configuration provided was successfully loaded"

================================================================================

PHASE 3: DETECTION RULES

Step 1: Create project folder
- Run: mkdir -p ~/nids-project/templates
- Run: cd ~/nids-project
- Run: code .

Step 2: Create local.rules file
- Run: sudo nano /etc/suricata/rules/local.rules
- Copy and paste these 10 rules:

+--------+----------------------+------------------------------------------------------------------+
| SID    | Attack Type          | Rule Content                                                     |
+--------+----------------------+------------------------------------------------------------------+
| 1000001| ICMP Ping Flood      | alert icmp any any -> $HOME_NET any (msg:"ICMP Ping Flood        |
|        |                      | Detected"; threshold: type both, track by_src, count 10,         |
|        |                      | seconds 5; sid:1000001; rev:1;)                                  |
+--------+----------------------+------------------------------------------------------------------+
| 1000002| TCP Port Scan        | alert tcp any any -> $HOME_NET any (msg:"TCP Port Scan Detected";|
|        |                      | flags:S; threshold: type threshold, track by_src, count 20,      |
|        |                      | seconds 10; sid:1000002; rev:1;)                                 |
+--------+----------------------+------------------------------------------------------------------+
| 1000003| SSH Brute Force      | alert tcp any any -> $HOME_NET 22 (msg:"SSH Brute Force Attempt";|
|        |                      | threshold: type both, track by_src, count 5, seconds 60;         |
|        |                      | sid:1000003; rev:1;)                                             |
+--------+----------------------+------------------------------------------------------------------+
| 1000004| SQL Injection        | alert http any any -> $HOME_NET any (msg:"SQL Injection Attempt -|
|        | (OR 1=1)             | OR 1=1"; content:"' OR '1'='1"; http_uri; nocase;                |
|        |                      | sid:1000004; rev:1;)                                             |
+--------+----------------------+------------------------------------------------------------------+
| 1000005| SQL Injection        | alert http any any -> $HOME_NET any (msg:"SQL Injection Attempt -|
|        | (UNION SELECT)       | UNION SELECT"; content:"UNION SELECT"; http_uri; nocase;         |
|        |                      | sid:1000005; rev:1;)                                             |
+--------+----------------------+------------------------------------------------------------------+
| 1000006| Telnet Attempt       | alert tcp any any -> $HOME_NET 23 (msg:"Telnet Connection        |
|        |                      | Attempt - Unencrypted Protocol"; sid:1000006; rev:1;)            |
+--------+----------------------+------------------------------------------------------------------+
| 1000007| FTP Brute Force      | alert tcp any any -> $HOME_NET 21 (msg:"FTP Brute Force Attempt";|
|        |                      | threshold: type both, track by_src, count 5, seconds 30;         |
|        |                      | sid:1000007; rev:1;)                                             |
+--------+----------------------+------------------------------------------------------------------+
| 1000008| Directory Traversal  | alert http any any -> $HOME_NET any (msg:"Directory Traversal    |
|        |                      | Attempt"; content:"../"; http_uri; sid:1000008; rev:1;)          |
+--------+----------------------+------------------------------------------------------------------+
| 1000009| XSS Attempt          | alert http any any -> $HOME_NET any (msg:"XSS Attempt Detected"; |
|        |                      | content:"<script>"; http_uri; nocase; sid:1000009; rev:1;)       |
+--------+----------------------+------------------------------------------------------------------+
| 1000010| RDP Brute Force      | alert tcp any any -> $HOME_NET 3389 (msg:"RDP Brute Force        |
|        |                      | Attempt"; threshold: type both, track by_src, count 5, seconds   |
|        |                      | 60; sid:1000010; rev:1;)                                         |
+--------+----------------------+------------------------------------------------------------------+

- Save with Ctrl+O then Enter, exit with Ctrl+X

Step 3: Register rules in suricata.yaml
- Run: sudo nano /etc/suricata/suricata.yaml
- Press Ctrl+W and search for "rule-files"
- Add a new line under suricata.rules with 2 spaces, a dash, a space, then local.rules
- Result should look like:
  rule-files:
    - suricata.rules
    - local.rules
- Save with Ctrl+O then Enter, exit with Ctrl+X

Step 4: Download community rules
- Run: sudo pip3 install suricata-update --break-system-packages
- Run: sudo suricata-update
- Expected output: "Loaded 45000 rules"

================================================================================

PHASE 4: CREATE PYTHON FILES

In VS Code with nids-project open, create three files:

+---------------------+---------------------------------------------------------------+
| File Name           | Description                                                   |
+---------------------+---------------------------------------------------------------+
| alert_monitor.py    | Watches eve.json and prints colored alerts in real-time      |
| dashboard_data.py   | Parses alerts and creates dashboard_data.json                |
| app.py              | Flask server that serves the dashboard                       |
+---------------------+---------------------------------------------------------------+

Creation steps:
- Click New File icon, name the file as shown above
- Paste the corresponding code from the original HTML document
- Press Ctrl+S to save each file

================================================================================

PHASE 5: CREATE DASHBOARD HTML

- Click the templates folder in VS Code Explorer to select it
- Click New File icon, name it dashboard.html
- Make sure it appears inside the templates folder
- Paste the complete dashboard.html code (HTML/CSS/JS dashboard with charts and table)
- Press Ctrl+S to save

Final project structure after Phase 5:

~/nids-project/
    |
    +-- alert_monitor.py
    +-- app.py
    +-- dashboard_data.py
    |
    +-- templates/
           |
           +-- dashboard.html

================================================================================

PHASE 6: LAUNCH THE SYSTEM

Before starting - create log permissions:
- Run: sudo mkdir -p /var/log/suricata
- Run: sudo chmod 755 /var/log/suricata
- Run: sudo touch /var/log/suricata/eve.json
- Run: sudo chmod 644 /var/log/suricata/eve.json

Open THREE Ubuntu terminals:

+-------------+----------------------------------------------------------+
| Terminal    | Command to Run                                           |
+-------------+----------------------------------------------------------+
| Terminal 1  | sudo suricata -c /etc/suricata/suricata.yaml -i eth0     |
| (Suricata)  | (replace eth0 with your interface name)                 |
|             | Expected: "all engines started"                         |
+-------------+----------------------------------------------------------+
| Terminal 2  | cd ~/nids-project                                        |
| (Monitor)   | python3 alert_monitor.py                                 |
|             | Expected: "Shield NIDS Monitor Running"                 |
+-------------+----------------------------------------------------------+
| Terminal 3  | cd ~/nids-project                                        |
| (Dashboard) | python3 app.py                                           |
|             | Expected: "Running on http://0.0.0.0:5000"              |
+-------------+----------------------------------------------------------+

Open browser to: http://localhost:5000

================================================================================

PHASE 7: SIMULATE ATTACKS

Open a FOURTH Ubuntu terminal:

Install testing tools: sudo apt install nmap hping3 -y

+--------------+---------------------+-------------------------------------------------+
| Test         | Command             | Expected Alert in Terminal 2                    |
+--------------+---------------------+-------------------------------------------------+
| Ping Flood   | ping -c 50 -i 0.05  | ICMP Ping Flood Detected                        |
|              | 127.0.0.1           |                                                 |
+--------------+---------------------+-------------------------------------------------+
| Port Scan    | sudo nmap -sS -p    | TCP Port Scan Detected                          |
|              | 1-1000 127.0.0.1    |                                                 |
+--------------+---------------------+-------------------------------------------------+
| SSH Brute    | for i in {1..10};   | SSH Brute Force Attempt                         |
| Force        | do ssh -o           |                                                 |
|              | ConnectTimeout=1    |                                                 |
|              | -o StrictHostKey    |                                                 |
|              | Checking=no root@   |                                                 |
|              | 127.0.0.1 2>/dev/   |                                                 |
|              | null; done          |                                                 |
+--------------+---------------------+-------------------------------------------------+
| SQL Injec-   | curl "http://       | SQL Injection Attempt - OR 1=1                  |
| tion         | 127.0.0.1/login?    | SQL Injection Attempt - UNION SELECT            |
|              | u=%27%20OR%20%271   |                                                 |
|              | %27%3D%271"         |                                                 |
+--------------+---------------------+-------------------------------------------------+

Verify on Dashboard:
- Go to http://localhost:5000
- Click Refresh Now or press F5
- Dashboard shows total alerts > 0, populated charts, and recent alerts table

Check raw logs:
- sudo cat /var/log/suricata/fast.log
- sudo cat /var/log/suricata/eve.json | python3 -m json.tool | grep -A2 '"event_type": "alert"'

================================================================================

PHASE 8: TROUBLESHOOTING

+-------------------------------------+------------------------------------------------+
| Problem                             | Solution                                       |
+-------------------------------------+------------------------------------------------+
| suricata: command not found         | sudo apt install suricata -y                  |
+-------------------------------------+------------------------------------------------+
| WSL shows version 1 instead of 2    | wsl --set-version Ubuntu-22.04 2              |
+-------------------------------------+------------------------------------------------+
| Permission denied on eve.json       | sudo chmod 644 /var/log/suricata/eve.json     |
+-------------------------------------+------------------------------------------------+
| Flask says Address already in use   | kill $(lsof -t -i:5000) then python3 app.py   |
+-------------------------------------+------------------------------------------------+
| TemplateNotFound: dashboard.html    | Run Flask from ~/nids-project and ensure      |
|                                     | dashboard.html is inside templates/ folder    |
+-------------------------------------+------------------------------------------------+
| ModuleNotFoundError: watchdog       | pip3 install watchdog --break-system-packages |
+-------------------------------------+------------------------------------------------+
| Suricata starts then immediately    | sudo suricata -c /etc/suricata/suricata.yaml  |
| exits                                | -i eth0 -v 2>&1 | head -50                    |
+-------------------------------------+------------------------------------------------+

================================================================================

TASK COMPLETION STATUS

+-------------------------------------+----------+
| Task                                | Status   |
+-------------------------------------+----------+
| Set up NIDS environment             | Complete |
| Configure rules and alerts          | Complete |
| Monitor network traffic             | Complete |
| Implement response mechanisms       | Complete |
| Visualize detected attacks          | Complete |
+-------------------------------------+----------+

================================================================================

AUTHOR: Cybersecurity Internship Project

LICENSE: Educational Use Only

================================================================================