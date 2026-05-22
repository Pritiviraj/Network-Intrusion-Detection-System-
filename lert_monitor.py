#!/usr/bin/env python3
"""
NIDS Alert Monitor - Watches Suricata eve.json in real time.
Prints color-coded alerts and auto-blocks critical source IPs.
"""
import json, time, os, subprocess
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

EVE_LOG = "/var/log/suricata/eve.json"
BLOCKED = set()

def block_ip(ip):
    if ip not in BLOCKED and not ip.startswith("127."):
        print(f"\n\033[91m[BLOCKING IP] {ip}\033[0m")
        subprocess.run(["sudo","iptables","-A","INPUT","-s",ip,"-j","DROP"])
        BLOCKED.add(ip)
        with open("response_log.txt","a") as f:
            f.write(f"[{datetime.now()}] BLOCKED: {ip}\n")

def print_alert(ev):
    a   = ev.get("alert", {})
    sev = a.get("severity", "?")
    src = ev.get("src_ip", "N/A")
    clr = "\033[91m" if sev==1 else ("\033[93m" if sev==2 else "\033[96m")
    rst = "\033[0m"
    print(f"{clr}")
    print(f"{'='*60}")
    print(f"  ALERT  |  Severity: {sev}")
    print(f"  Time   : {ev.get('timestamp','')}")
    print(f"  Source : {src}:{ev.get('src_port','')}")
    print(f"  Dest   : {ev.get('dest_ip','')}:{ev.get('dest_port','')}")
    print(f"  Rule   : {a.get('signature','')}")
    print(f"  Cat    : {a.get('category','')}")
    print(f"{'='*60}{rst}")
    if sev == 1:
        block_ip(src)

class LogWatcher(FileSystemEventHandler):
    def __init__(self):
        self._pos = os.path.getsize(EVE_LOG) if os.path.exists(EVE_LOG) else 0
    def on_modified(self, event):
        if "eve.json" not in event.src_path:
            return
        with open(EVE_LOG) as f:
            f.seek(self._pos)
            for line in f:
                try:
                    ev = json.loads(line)
                    if ev.get("event_type") == "alert":
                        print_alert(ev)
                except:
                    pass
            self._pos = f.tell()

if __name__ == "__main__":
    print("Shield NIDS Monitor Running - Ctrl+C to stop\n")
    if not os.path.exists(EVE_LOG):
        print(f"[WARN] Log not found yet: {EVE_LOG}")
        print("[INFO] Suricata must be running to generate logs\n")
    obs = Observer()
    obs.schedule(LogWatcher(), path="/var/log/suricata/", recursive=False)
    obs.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        obs.stop()
        print("\nMonitor stopped.")
    obs.join()