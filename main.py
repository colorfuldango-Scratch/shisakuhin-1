import os
import time
from threading import Thread
from flask import Flask
import scratchattach as scratch3

# 1. Renderの強制終了を防ぐためのダミーWebサーバー
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 scratchattach bot is running 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# バックグラウンドでダミーサーバーを起動
Thread(target=run_flask, daemon=True).start()

# ==========================================
# ⚡ 2. 本命の scratchattach アタッチ呼び出し
# ==========================================
PROJECT_ID = "YOUR_PROJECT_ID"
SESSION_ID = os.environ.get("SCRATCH_SESSION_ID", "YOUR_SESSION_ID")
USERNAME = "YOUR_USERNAME"

print("🚀 scratchattach を起動中...")

# Scratchに接続
session = scratch3.Session(SESSION_ID, username=USERNAME)
conn = session.connect_cloud(PROJECT_ID)

# イベントハンドラー（アタッチ機能）を生成
events = scratch3.CloudEvents(PROJECT_ID)

@events.event
def on_set(event):
    """Scratch側でクラウド変数が変わったら自動で呼び出されるアタッチ関数"""
    if event.var == "prompt_request" and event.value != "0":
        print(f"📥 【Scratchから検知】プロンプトが来ました: {event.value}")
        # ここにWebLLM（ブラウザ）へ通知したり処理を回すコードを入れます

@events.event
def on_ready():
    print("✅ Scratchアタッチ完了！常時監視ループに入りました！")

# 🏁 これが scratchattach の常時実行（更新）を呼び出すコマンド！
events.start()

# Renderが終了しないようにメインスレッドを維持
while True:
    time.sleep(1)
