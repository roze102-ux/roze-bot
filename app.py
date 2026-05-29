from flask import Flask, request, jsonify, render_template_string
import anthropic
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

conversation = []

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>My AI Chatbot</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; background: #f5f5f5; }
        h1 { color: #333; }
        #chat-box { background: white; border-radius: 10px; padding: 20px; height: 400px; overflow-y: auto; margin-bottom: 20px; border: 1px solid #ddd; }
        .user-msg { text-align: right; margin: 10px 0; }
        .user-msg span { background: #0084ff; color: white; padding: 8px 14px; border-radius: 18px; display: inline-block; max-width: 70%; }
        .bot-msg { text-align: left; margin: 10px 0; }
        .bot-msg span { background: #e4e6eb; color: #333; padding: 8px 14px; border-radius: 18px; display: inline-block; max-width: 70%; }
        #input-area { display: flex; gap: 10px; }
        #user-input { flex: 1; padding: 12px; border-radius: 25px; border: 1px solid #ddd; font-size: 16px; outline: none; }
        #send-btn { padding: 12px 24px; background: #0084ff; color: white; border: none; border-radius: 25px; cursor: pointer; font-size: 16px; }
        #send-btn:hover { background: #0066cc; }
    </style>
</head>
<body>
    <h1>🤖 My AI Chatbot</h1>
    <div id="chat-box"></div>
    <div id="input-area">
        <input type="text" id="user-input" placeholder="Type a message..." />
        <button id="send-btn" onclick="sendMessage()">Send</button>
    </div>
    <script>
        function sendMessage() {
            const input = document.getElementById("user-input");
            const msg = input.value.trim();
            if (!msg) return;
            appendMessage("user", msg);
            input.value = "";
            fetch("/chat", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ message: msg }) })
            .then(r => r.json()).then(data => appendMessage("bot", data.reply));
        }
        function appendMessage(role, text) {
            const box = document.getElementById("chat-box");
            const div = document.createElement("div");
            div.className = role === "user" ? "user-msg" : "bot-msg";
            div.innerHTML = `<span>${text}</span>`;
            box.appendChild(div);
            box.scrollTop = box.scrollHeight;
        }
        document.getElementById("user-input").addEventListener("keypress", function(e) {
            if (e.key === "Enter") sendMessage();
        });
    </script>
</body>
</html>
'''

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    conversation.append({"role": "user", "content": user_input})
    response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1000,
    system="You are Roze-Bot, a friendly and warm personal coach. You were built by a developer named Roze. You are encouraging, supportive, and genuinely care about helping people reach their goals. You ask thoughtful questions to understand what someone needs, celebrate their wins no matter how small, and gently motivate them when they're struggling. You speak warmly like a trusted friend who happens to be a great coach.",
    messages=conversation
)
    reply = response.content[0].text
    conversation.append({"role": "assistant", "content": reply})
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)