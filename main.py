"""
arXiv論文検索メインプログラム
"""
from arxiv_search import search_papers_by_date
from date_utils import get_date_range


def display_results(results):
    """
    検索結果を表示する関数
    
    Args:
        results: 検索結果のリスト
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
            #print(f"   要約: {result.summary}")
    else:
        print("検索結果がありませんでした。")


if __name__ == "__main__":
    # ===== 検索パラメータ =====
    # モード選択: "auto" (前日を自動計算) または "manual" (手動で日付を指定)
    date_mode = "auto"  # "auto" または "manual" を選択
    
    # 手動モードの場合の日付設定
    manual_start_date = "20240923"  # 検索開始日（YYYYMMDD形式）
    manual_end_date = "20241023"    # 検索終了日（YYYYMMDD形式）
    
    max_results = 100   # 最大結果数
    
    # ===== 日付範囲の取得 =====
    if date_mode == "auto":
        target_date, end_target = get_date_range(mode="auto")
    else:
        target_date, end_target = get_date_range(
            mode="manual",
            start_date=manual_start_date,
            end_date=manual_end_date
        )
    
    # ===== 検索実行 =====
    results = search_papers_by_date(
        start_date=target_date,
        end_date=end_target,
        max_results=max_results
    )
    
    # ===== 結果表示 =====
    display_results(results)

