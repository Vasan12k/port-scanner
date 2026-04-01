from flask import Flask, jsonify, request, render_template
from scanner import scan_target
import os

app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), 'static'))

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    try:
        data = request.json or {}
        target = data.get("target", "").strip()
        start_port = int(data.get("start_port", 1))
        end_port = int(data.get("end_port", 100))
        timeout = float(data.get("timeout", 0.5))

        if not target:
            return jsonify({"error": "Target is required"}), 400

        open_ports = scan_target(target, start_port, end_port, timeout)
        return jsonify({"target": target, "open_ports": open_ports}), 200
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
