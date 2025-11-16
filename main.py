"""
arXiv論文検索メインプログラム
"""
from typing import Optional, List
import arxiv
from arxiv_search import search_papers_by_date
from date_utils import get_date_range, DATE_MODE_AUTO, DATE_MODE_MANUAL
from gemini_module import classify_genre


# 定数定義
MAX_AUTHORS_DISPLAY = 3


def format_author_list(authors: List, max_count: int = MAX_AUTHORS_DISPLAY) -> str:
    """
    著者リストをフォーマットする
    
    Args:
        authors: 著者リスト
        max_count: 表示する最大著者数
    
    Returns:
        フォーマット済みの著者文字列
    """
    author_strs = [str(author) for author in authors[:max_count]]
    return ', '.join(author_strs)


def format_category_list(categories: List) -> str:
    """
    カテゴリーリストをフォーマットする
    
    Args:
        categories: カテゴリーリスト
    
    Returns:
        フォーマット済みのカテゴリー文字列
    """
    return ', '.join([str(cat) for cat in categories])


def classify_paper_genre(
    genre: str,
    abstract: str
) -> Optional[str]:
    """
    論文のジャンルを判定する（エラーハンドリング付き）
    
    Args:
        genre: 判定したいジャンル名
        abstract: 論文のアブストラクト
    
    Returns:
        判定結果（"Yes" または "No"）、エラー時はNone
    """
    try:
        return classify_genre(genre, abstract)
    except RuntimeError as e:
        print(f"   Gemini判定エラー: {e}")
        return None
    except Exception as e:
        print(f"   Gemini判定エラー: {str(e)}")
        return None


def display_results(
    results: List[arxiv.Result],
    genre: Optional[str] = None,
    enable_gemini: bool = False
) -> None:
    """
    検索結果を表示する関数
    
    Args:
        results: 検索結果のリスト
        genre: Geminiで判定するジャンル（Noneの場合は判定しない）
        enable_gemini: Gemini判定を有効にするかどうか
    """
    print(f"検索結果数: {len(results)}")

    if not results:
        print("検索結果がありませんでした。")
        return
    
    # すべての結果を表示
    print(f"\n=== 検索結果一覧 ===")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result.title}")
        print(f"   著者: {format_author_list(result.authors)}")
        print(f"   カテゴリー: {format_category_list(result.categories)}")
        print(f"   URL: {result.entry_id}")
        
        # Gemini判定を実行
        if enable_gemini and genre and result.summary:
            classification = classify_paper_genre(genre, result.summary)
            if classification:
                print(f"   Gemini判定（{genre}）: {classification}")


if __name__ == "__main__":
    # ===== 検索パラメータ =====
    # モード選択: "auto" (前日を自動計算) または "manual" (手動で日付を指定)
    DATE_MODE = DATE_MODE_MANUAL
    
    # 手動モードの場合の日付設定
    MANUAL_START_DATE = "20240923"  # 検索開始日（YYYYMMDD形式）
    MANUAL_END_DATE = "20241023"    # 検索終了日（YYYYMMDD形式）
    
    MAX_RESULTS = 10   # 最大結果数
    
    # ===== Gemini判定設定 =====
    ENABLE_GEMINI = True  # Gemini判定を有効にするかどうか
    TARGET_GENRE = "自動運転"  # 判定したいジャンル名（Noneの場合は判定しない）
    
    # ===== 日付範囲の取得 =====
    if DATE_MODE == DATE_MODE_AUTO:
        target_date, end_target = get_date_range(mode=DATE_MODE_AUTO)
    else:
        target_date, end_target = get_date_range(
            mode=DATE_MODE_MANUAL,
            start_date=MANUAL_START_DATE,
            end_date=MANUAL_END_DATE
        )
    
    # ===== 検索実行 =====
    results = search_papers_by_date(
        start_date=target_date,
        end_date=end_target,
        max_results=MAX_RESULTS
    )
    
    # ===== 結果表示（Gemini判定含む） =====
    display_results(
        results,
        genre=TARGET_GENRE if ENABLE_GEMINI else None,
        enable_gemini=ENABLE_GEMINI
    )

