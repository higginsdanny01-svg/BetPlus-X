import os
import sqlite3
from flask import Flask, request, render_template_string
from telegram import Bot
import random
import string

app = Flask(__name__)

# ================== CONFIG ==================
BOT_TOKEN = "8701765620:AAEYuEy6VQ4q85cVdc_VTDXGIqQiJM8ivP0"  # ⚠️ Exposed (not recommended)
bot = Bot(token=BOT_TOKEN)

# ================== HTML ==================
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Access Page</title>
</head>
<body>
    <h2>Enter Access Code</h2>
    <form method="POST">
        <input name="code" required>
        <button type="submit">Submit</button>
    </form>
    <p>{{msg}}</p>
</body>
</html>
"""

# ================== DATABASE ==================
def init_db():
    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS codes (
            code TEXT PRIMARY KEY,
            used INTEGER DEFAULT 0
        )
        """)
        conn.commit()

init_db()

# ================== WEBSITE ==================
@app.route("/", methods=["GET", "POST"])
def home():
    msg = ""

    if request.method == "POST":
        code = request.form["code"]

        with sqlite3.connect("database.db") as conn:
            c = conn.cursor()

            c.execute("SELECT used FROM codes WHERE code=?", (code,))
            res = c.fetchone()

            if res and res[0] == 0:
                c.execute("UPDATE codes SET used=1 WHERE code=?", (code,))
                conn.commit()
                msg = "✅ Access Granted"
            else:
                msg = "❌ Invalid or Already Used Code"

    return render_template_string(HTML, msg=msg)

# ================== TELEGRAM WEBHOOK ==================
@app.route(f"/bot{BOT_TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.get_json()

    if data and "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text == "/start":
            bot.send_message(chat_id=chat_id, text="Welcome! Send /code to get access code")

        elif text == "/code":
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

            with sqlite3.connect("database.db") as conn:
                c = conn.cursor()
                c.execute("INSERT INTO codes (code, used) VALUES (?, 0)", (code,))
                conn.commit()

            bot.send_message(chat_id=chat_id, text=f"🎟 Your Code: {code}")

        else:
            bot.send_message(chat_id=chat_id, text="Unknown command")

    return "OK"

# ================== SET WEBHOOK ==================
@app.route("/set_webhook")
def set_webhook():
    url = os.getenv("RENDER_EXTERNAL_URL")

    webhook_url = f"{url}/bot{BOT_TOKEN}"
    bot.set_webhook(webhook_url)

    return f"Webhook set to {webhook_url}"

# ================== RUN ==================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))            else:
                msg = "❌ Invalid or Already Used Code"

    return render_template_string(HTML, msg=msg)

# ================== TELEGRAM WEBHOOK ==================
@app.route(f"/bot{BOT_TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text == "/start":
            bot.send_message(chat_id=chat_id, text="Send /code to get a new access code")

        elif text == "/code":
            import random
            import string

            # Generate random code
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

            with sqlite3.connect("database.db") as conn:
                c = conn.cursor()
                c.execute("INSERT INTO codes (code, used) VALUES (?, 0)", (code,))
                conn.commit()

            bot.send_message(chat_id=chat_id, text=f"Your code: {code}")

        else:
            bot.send_message(chat_id=chat_id, text="Unknown command")

    return "OK"

# ================== SET WEBHOOK ==================
@app.route("/set_webhook/<secret>")
def set_webhook(secret):
    if secret != "12345":  # change this!
        return "Unauthorized"

    url = os.getenv("RENDER_EXTERNAL_URL")
    webhook_url = f"{url}/bot{BOT_TOKEN}"

    bot.set_webhook(webhook_url)

    return f"Webhook set to {webhook_url}"

# ================== RUN ==================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
