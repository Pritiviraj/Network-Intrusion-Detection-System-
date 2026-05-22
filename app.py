#!/usr/bin/env python3
from flask import Flask, render_template, jsonify
import json, os

app = Flask(__name__)

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/api/data")
def api_data():
    # Re-parse logs every time the page refreshes
    os.system(f"python3 {PROJECT_DIR}/dashboard_data.py")
    data_file = os.path.join(PROJECT_DIR, "dashboard_data.json")
    try:
        with open(data_file) as f:
            return jsonify(json.load(f))
    except FileNotFoundError:
        return jsonify({
            "total_alerts": 0, "unique_attackers": 0,
            "top_signatures": [], "by_category": [],
            "by_severity": {}, "recent_alerts": [],
            "top_src_ips": [], "by_protocol": {}
        })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)