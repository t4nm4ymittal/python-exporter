from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

# OpenShift API URL for pod metrics
API_URL = "https://openshift.default.svc/apis/metrics.k8s.io/v1beta1/namespaces/t4nm4y-dev/pods"

# Load OpenShift Token from mounted service account
with open("/var/run/secrets/kubernetes.io/serviceaccount/token", "r") as f:
    OPENSHIFT_TOKEN = f.read().strip()

HEADERS = {"Authorization": f"Bearer {OPENSHIFT_TOKEN}"}

@app.route("/metrics", methods=["GET"])
def get_metrics():
    try:
        response = requests.get(API_URL, headers=HEADERS, verify=False)
        data = response.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
