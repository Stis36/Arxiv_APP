# gemini_simple.py

import os
import google.generativeai as genai

# ① OS の環境変数 GEMINI_API_KEY から取得する
API_KEY = os.getenv("GEMINI_API_KEY")

# ② 使いたいモデル名（よく使われるのは gemini-1.5-flash / gemini-1.5-pro など）
MODEL_NAME = "gemini-2.5-flash"

def main():
    # API キーの存在チェック（任意）
    if API_KEY is None:
        raise RuntimeError("環境変数 GEMINI_API_KEY が設定されていません。")

    # API キーを設定
    genai.configure(api_key=API_KEY)

    # モデルを作成
    model = genai.GenerativeModel(MODEL_NAME)

    # プロンプト（好きに変えてOK）
    prompt = "Please talk about the latest research in the field of AI. in 100 words."

    # テキスト生成を実行
    response = model.generate_content(prompt)

    # 結果を表示
    print("=== Gemini からの回答 ===")
    print(response.text)

if __name__ == "__main__":
    main()