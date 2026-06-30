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

# --- Scratch用エンコーダー / デコーダー ---
CHARS = " あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんーがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽっゃゅょ？！。、0123456789abcdefghijklmnopqrstuvwxyz"

def decode(encoded_str):
    text = ""
    try:
        for i in range(0, len(encoded_str), 2):
            index = int(encoded_str[i:i+2])
            if index < len(CHARS):
                text += CHARS[index]
    except Exception:
        return "デコードエラー"
    return text

def encode(text):
    encoded = ""
    text = text.lower()
    for char in text:
        if char in CHARS:
            index = CHARS.index(char)
            encoded += f"{index:02d}"
        else:
            encoded += "01"
    return encoded

# --- Flaskの設定 ---
@app.route('/')
def home():
    return "Scratch AI Bot (Numeric Version) is Running!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# --- Scratch & Hugging Face 連動処理 ---
if SESSION_ID:
    try:
        print("🚀 scratchattach と Hugging Face Client を起動中...")
        
        # 【修正箇所】キーワード引数を使わず、順番だけで安全に指定
        session = scratch3.Session(SESSION_ID, USERNAME)
        conn = session.connect_cloud(project_id=PROJECT_ID)
        
        hf_client = Client("huggingface-projects/gemma-4-12b-it")
        client = scratch3.CloudRequests(conn)

        @client.request
        def ai_chat(encoded_prompt):
            prompt = decode(str(encoded_prompt))
            print(f"💬 Scratch（数字）を受信 -> 翻訳: {prompt}")
            
            try:
                result = hf_client.predict(
                    message=prompt,
                    chat_history=[],
                    system_prompt="あなたは親切なAIアシスタントです。漢字は絶対に使わず、すべてひらがなとカタカナ、数字のみで、30文字以内で短く簡潔に答えてください。",
                    api_name="/chat"
                )
                print(f"🤖 Gemmaからの返答（原文）: {result}")
                
                encoded_result = encode(result)
                print(f"➡️ 返答を数字に変換 -> Scratchへ送信: {encoded_result}")
                return encoded_result
                
            except Exception as e:
                print(f"❌ AI呼び出しエラー: {e}")
                return encode("えらーがおきたよ")

        client.start(thread=True)
        print("✅ 数字対応版のCloudRequestsが起動しました！")
        
    except Exception as e:
        print(f"❌ 起動エラー: {e}")
else:
    print("⚠️ SCRATCH_SESSION_ID が環境変数に設定されていません。")

if __name__ == "__main__":
    run_flask()
