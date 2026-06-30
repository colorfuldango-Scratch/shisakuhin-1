import os
from flask import Flask
import scratchattach as scratch3
from gradio_client import Client

app = Flask(__name__)

# --- 設定部分 ---
# ※ ユーザー名とプロジェクトIDは君のものに書き換えてね！
USERNAME = "colorfuldango" 
PROJECT_ID = "1350190285"  # 君のScratchのプロジェクトID（数字）に変えてね

# Renderの環境変数からセッションIDを読み込む
SESSION_ID = os.environ.get("SCRATCH_SESSION_ID")

@app.route('/')
def home():
    return "Scratch Bot with Gemma 4 is Running!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# --- Scratch & Hugging Face 連動処理 ---
if SESSION_ID:
    try:
        print("🚀 scratchattach と Hugging Face Client を起動中...")
        
        # Scratchのセッションと接続
        session = scratch3.Session(SESSION_ID, username=USERNAME)
        conn = session.connect_cloud(project_id=PROJECT_ID)
        
        # Hugging FaceのGemma 4のデモSpaceに接続
        hf_client = Client("huggingface-projects/gemma-4-12b-it")
        
        # Scratchからのリクエストを受け付ける枠組みを作る
        client = scratch3.CloudRequests(conn)

        # Scratchから「ai_chat」というリクエストが来たら実行する関数
        @client.request
        def ai_chat(prompt):
            print(f"💬 Scratchからプロンプトを受信: {prompt}")
            try:
                # 指定されたGemma 4のAPIにプロンプトを投げて返事をもらう
                # ※第2引数はチャット履歴（最初は空でOK）、第3引数はシステムプロンプト
                result = hf_client.predict(
                    message=prompt,
                    chat_history=[],
                    system_prompt="あなたは親切なAIアシスタントです。日本語で短く簡潔に答えてください。",
                    api_name="/chat"
                )
                print(f"🤖 Gemmaからの返答: {result}")
                return result # Scratchに返事の文字が自動で送り返されるよ
            except Exception as e:
                print(f"❌ AI呼び出しエラー: {e}")
                return "AIの呼び出しに失敗したよ"

        # バックグラウンドでScratchの見張りをスタート
        client.start(thread=True)
        print("✅ Scratchのクラウド変数（CloudRequests）が起動しました！接続完了！")
        
    except Exception as e:
        print(f"❌ 起動エラー: {e}")
else:
    print("⚠️ SCRATCH_SESSION_ID が環境変数に設定されていません。")

# --- サーバー起動 ---
if __name__ == "__main__":
    run_flask()
