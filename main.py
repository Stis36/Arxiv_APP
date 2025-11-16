"""
arXiv論文検索メインプログラム
"""
from arxiv_search import search_papers_by_date
from date_utils import get_date_range
from gemini_module import classify_genre


def display_results(results, genre=None, enable_gemini=False):
    """
    検索結果を表示する関数
    
    Args:
        results: 検索結果のリスト
        genre: Geminiで判定するジャンル（Noneの場合は判定しない）
        enable_gemini: Gemini判定を有効にするかどうか
    """
    print(f"検索結果数: {len(results)}")

    if results:
        # すべての結果を表示
        print(f"\n=== 検索結果一覧 ===")
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result.title}")
            print(f"   著者: {', '.join([str(author) for author in result.authors[:3]])}")
            print(f"   カテゴリー: {', '.join([str(cat) for cat in result.categories])}")
            print(f"   URL: {result.entry_id}")
            
            # Gemini判定を実行
            if enable_gemini and genre and result.summary:
                try:
                    classification = classify_genre(genre, result.summary)
                    print(f"   Gemini判定（{genre}）: {classification}")
                except RuntimeError as e:
                    print(f"   Gemini判定エラー: {e}")
                except Exception as e:
                    print(f"   Gemini判定エラー: {str(e)}")
    else:
        print("検索結果がありませんでした。")


if __name__ == "__main__":
    # ===== 検索パラメータ =====
    # モード選択: "auto" (前日を自動計算) または "manual" (手動で日付を指定)
    date_mode = "manual"  # "auto" または "manual" を選択
    
    # 手動モードの場合の日付設定
    manual_start_date = "20240923"  # 検索開始日（YYYYMMDD形式）
    manual_end_date = "20241023"    # 検索終了日（YYYYMMDD形式）
    
    max_results = 10   # 最大結果数
    
    # ===== 日付範囲の取得 =====
    if date_mode == "auto":
        target_date, end_target = get_date_range(mode="auto")
    else:
        target_date, end_target = get_date_range(
            mode="manual",
            start_date=manual_start_date,
            end_date=manual_end_date
        )
    
    # ===== Gemini判定設定 =====
    enable_gemini = True  # Gemini判定を有効にするかどうか
    target_genre = "自動運転"  # 判定したいジャンル名（Noneの場合は判定しない）
    
    # ===== 検索実行 =====
    results = search_papers_by_date(
        start_date=target_date,
        end_date=end_target,
        max_results=max_results
    )
    
    # ===== 結果表示（Gemini判定含む） =====
    display_results(results, genre=target_genre, enable_gemini=enable_gemini)

