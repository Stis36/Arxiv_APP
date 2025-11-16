# Arxiv_APP

arXivから新規発行された論文を取得し、Gemini APIを使用してジャンル分類を行うアプリケーションです。

## 機能

- **arXiv論文検索**: 指定した日付範囲でarXiv論文を検索
- **自動日付モード**: 前日の日付を自動計算して検索
- **手動日付モード**: 任意の日付範囲を指定して検索
- **Geminiジャンル分類**: 論文のアブストラクトをGemini APIで分析し、指定したジャンルに該当するかを判定

## 必要な環境

- Python 3.7以上
- 以下のPythonパッケージ:
  - `arxiv` - arXiv APIクライアント
  - `google-generativeai` - Gemini APIクライアント
  - `streamlit` - Web UIフレームワーク（Web UIを使用する場合）

## セットアップ

### 1. 依存パッケージのインストール

**コマンドライン版の場合:**
```bash
pip install arxiv google-generativeai
```

**Web UI版の場合:**
```bash
pip install -r requirements.txt
```

または個別にインストール:
```bash
pip install arxiv google-generativeai streamlit
```

### 2. 環境変数の設定

Gemini APIを使用する場合は、環境変数にAPIキーを設定してください：

```bash
export GEMINI_API_KEY="your-api-key-here"
```

または、`.env`ファイルを使用する場合は、適切なライブラリ（例: `python-dotenv`）を使用してください。

## 使用方法

### Web UI版（推奨）

Streamlitを使用したWebインターフェースを提供しています。

```bash
streamlit run app.py
```

ブラウザが自動的に開き、以下の機能が利用できます：

- **サイドバーで検索設定**
  - 日付モード（自動/手動）の選択
  - 日付範囲の指定（手動モードの場合）
  - 最大結果数の設定
  - Gemini判定の有効/無効
  - 判定したいジャンルの指定

- **検索結果の表示**
  - 論文タイトル、著者、カテゴリー
  - アブストラクトの表示/非表示
  - Gemini判定結果（該当/非該当）
  - 判定結果の統計情報

### コマンドライン版

```bash
python main.py
```

### 設定の変更

`main.py`の以下の設定を変更することで、動作をカスタマイズできます：

```python
# 日付モードの選択
DATE_MODE = DATE_MODE_AUTO    # 前日を自動計算
# DATE_MODE = DATE_MODE_MANUAL  # 手動で日付を指定

# 手動モードの場合の日付設定
MANUAL_START_DATE = "20240923"  # 検索開始日（YYYYMMDD形式）
MANUAL_END_DATE = "20241023"    # 検索終了日（YYYYMMDD形式）

# 最大結果数
MAX_RESULTS = 10

# Gemini判定設定
ENABLE_GEMINI = True           # Gemini判定を有効にするかどうか
TARGET_GENRE = "自動運転"      # 判定したいジャンル名
```

## モジュール構成

### `app.py`
Streamlitを使用したWeb UIアプリケーション。ブラウザベースのインターフェースを提供。

### `main.py`
コマンドライン版のメインプログラム。検索パラメータの設定、検索実行、結果表示を担当。

### `arxiv_search.py`
arXiv論文検索モジュール。
- `search_papers_by_date()`: 日付範囲でarXiv論文を検索

### `date_utils.py`
日付設定ユーティリティモジュール。
- `get_date_range()`: 日付範囲を取得（自動/手動モード対応）

### `gemini_module.py`
Gemini APIを使用した論文ジャンル分類モジュール。
- `classify_genre()`: 論文のアブストラクトが指定されたジャンルに該当するかを判定
- `create_prompt()`: ジャンル分類用のプロンプトを生成
- `get_gemini_response()`: Gemini APIを使用してテキスト生成を実行

## 出力例

```
検索結果数: 10

=== 検索結果一覧 ===

1. Example Paper Title
   著者: Author1, Author2, Author3
   カテゴリー: cs.AI, cs.LG
   URL: http://arxiv.org/abs/2024.12345
   Gemini判定（自動運転）: Yes

2. Another Paper Title
   著者: Author4, Author5
   カテゴリー: cs.CV
   URL: http://arxiv.org/abs/2024.12346
   Gemini判定（自動運転）: No
```


<img width="667" height="215" alt="スクリーンショット 2025-11-15 18 24 07" src="https://github.com/user-attachments/assets/2db6575a-93a3-408f-8bdd-45df0c0244bb" />

