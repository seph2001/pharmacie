from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "notifier"}), 200


@app.route("/notify", methods=["POST"])
def notify():
    data = request.get_json(force=True, silent=True) or {}
    phone = data.get("phone", "")
    email = data.get("email", "")
    message = data.get("message", "")
    
    if email:
        print(f"[NOTIFIER] -> EMAIL to {email}: {message}")
    if phone:
        print(f"[NOTIFIER] -> SMS to {phone}: {message}")
        
    return jsonify({"status": "sent"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
