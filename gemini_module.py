"""
Gemini API を使用した論文ジャンル分類モジュール
"""
import os
import google.generativeai as genai


# デフォルト設定
DEFAULT_MODEL_NAME = "gemini-2.5-flash"


def create_prompt(genre, abstract):
    """
    ジャンル分類用のプロンプトを生成する関数
    
    Args:
        genre: 判定したいジャンル名
        abstract: 論文のアブストラクト
    
    Returns:
        フォーマット済みのプロンプト文字列
    """
    prompt = (
        "以下に論文のアブストラクトを示す。内容が「{genre}」のジャンルとして該当するかどうかを、"
        "厳密な内容理解に基づいて Yes または No のみ で回答せよ。"
        "説明・推論・補足は一切不要。"
        "判断に迷う場合でも、アブストラクトの内容に最も整合的な方を選ぶこと。"
        "\n\n"
        "アブストラクト: {abstract}"
    ).format(genre=genre, abstract=abstract)
    
    return prompt


def get_gemini_response(prompt, api_key=None, model_name=None):
    """
    Gemini APIを使用してテキスト生成を実行する関数
    
    Args:
        prompt: 送信するプロンプト
        api_key: APIキー（Noneの場合は環境変数から取得）
        model_name: モデル名（Noneの場合はデフォルト値を使用）
    
    Returns:
        Geminiからの応答テキスト
    
    Raises:
        RuntimeError: APIキーが設定されていない場合
    """
    # APIキーの取得
    if api_key is None:
        api_key = os.getenv("GEMINI_API_KEY")
    
    if api_key is None:
        raise RuntimeError("環境変数 GEMINI_API_KEY が設定されていません。")
    
    # モデル名の設定
    if model_name is None:
        model_name = DEFAULT_MODEL_NAME
    
    # API キーを設定
    genai.configure(api_key=api_key)
    
    # モデルを作成
    model = genai.GenerativeModel(model_name)
    
    # テキスト生成を実行
    response = model.generate_content(prompt)
    
    return response.text


def classify_genre(genre, abstract, api_key=None, model_name=None):
    """
    論文のアブストラクトが指定されたジャンルに該当するかを判定する関数
    
    Args:
        genre: 判定したいジャンル名
        abstract: 論文のアブストラクト
        api_key: APIキー（Noneの場合は環境変数から取得）
        model_name: モデル名（Noneの場合はデフォルト値を使用）
    
    Returns:
        "Yes" または "No" の文字列
    
    Raises:
        RuntimeError: APIキーが設定されていない場合
    """
    prompt = create_prompt(genre, abstract)
    response = get_gemini_response(prompt, api_key=api_key, model_name=model_name)
    return response.strip()

