#!/usr/bin/env python3
"""
Reads Suricata's eve.json, extracts all alert events,
and writes dashboard_data.json for the Flask dashboard.
"""
import json, os
from collections import Counter
from datetime import datetime

EVE_LOG = "/var/log/suricata/eve.json"

def parse_alerts():
    alerts = []
    if not os.path.exists(EVE_LOG):
        return alerts
    with open(EVE_LOG) as f:
        for line in f:
            try:
                ev = json.loads(line)
                if ev.get("event_type") != "alert":
                    continue
                alerts.append({
                    "timestamp" : ev.get("timestamp"),
                    "src_ip"    : ev.get("src_ip"),
                    "dest_ip"   : ev.get("dest_ip"),
                    "dest_port" : ev.get("dest_port"),
                    "proto"     : ev.get("proto"),
                    "signature" : ev.get("alert", {}).get("signature"),
                    "severity"  : ev.get("alert", {}).get("severity"),
                    "category"  : ev.get("alert", {}).get("category"),
                })
            except:
                pass
    return alerts

def build_summary(alerts):
    sigs   = Counter(a["signature"] for a in alerts if a["signature"])
    ips    = Counter(a["src_ip"]    for a in alerts if a["src_ip"])
    cats   = Counter(a["category"]  for a in alerts if a["category"])
    sevs   = Counter(str(a["severity"]) for a in alerts if a["severity"])
    protos = Counter(a["proto"] for a in alerts if a["proto"])
    return {
        "generated_at"     : str(datetime.now()),
        "total_alerts"     : len(alerts),
        "unique_attackers" : len(ips),
        "top_signatures"   : sigs.most_common(10),
        "top_src_ips"      : ips.most_common(10),
        "by_category"      : cats.most_common(),
        "by_severity"      : dict(sevs),
        "by_protocol"      : dict(protos),
        "recent_alerts"    : alerts[-25:][::-1],
    }

if __name__ == "__main__":
    alerts  = parse_alerts()
    summary = build_summary(alerts)
    with open("dashboard_data.json","w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"[OK] {len(alerts)} alerts parsed -> dashboard_data.json")