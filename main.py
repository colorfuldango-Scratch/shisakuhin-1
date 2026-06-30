import os
from flask import Flask
import scratchattach as scratch3

app = Flask(__name__)

# --- 設定部分 ---
# ※ ユーザー名とプロジェクトIDは君のものに書き換えてね！
USERNAME = "colorfuldango" 
PROJECT_ID = "1350190285"  # 君のScratchのプロジェクトID（数字）に変えてね

# Renderの環境変数からセッションIDを読み込む
SESSION_ID = os.environ.get("SCRATCH_SESSION_ID")

@app.route('/')
def home():
    return "Scratch Bot is Running!"

def run_flask():
    # Renderが指定するポート、または5000番でFlaskを起動
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# --- Scratchの連動処理 ---
if SESSION_ID:
    try:
        print("🚀 scratchattach を起動中...")
        # 最新版の scratchattach に合わせた正しい書き方
        session = scratch3.Session(session_id=SESSION_ID, username=USERNAME)
        conn = session.connect_cloud(project_id=PROJECT_ID)
        
        # 例: クラウド変数「test」に「1」を書き込む（動作テスト用）
        # conn.set_var("test", 1)
        print("✅ Scratchのクラウド変数に接続しました！")
        
    except Exception as e:
        print(f"❌ Scratch接続エラー: {e}")
else:
    print("⚠️ SCRATCH_SESSION_ID が環境変数に設定されていません。")

# --- サーバー起動 ---
if __name__ == "__main__":
    run_flask()
