import socket
import threading
import webbrowser

from flask import Flask, jsonify, render_template, request

from chatbot import Chatbot

app = Flask(__name__)
bot = Chatbot()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    if not message:
        return jsonify({"error": "Empty message"}), 400
    # Browser-supplied local time/date (keeps the time correct on cloud servers)
    client_time = str(data.get("client_time") or "")[:30]
    client_date = str(data.get("client_date") or "")[:40]
    return jsonify(bot.respond(message, client_time, client_date))


def find_free_port(start=5000, tries=20):
    for port in range(start, start + tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
    return start


if __name__ == "__main__":
    port = find_free_port()
    url = f"http://127.0.0.1:{port}"
    print(f"\nChatbot running at {url}  (press Ctrl+C to stop)\n")
    threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    app.run(host="127.0.0.1", port=port, debug=False)
