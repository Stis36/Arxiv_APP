import arxiv
from datetime import datetime


def search_papers_by_date(start_date=None, end_date=None, max_results=10):
    """
    特定の日付範囲でarXiv論文を検索する関数
    
    Args:
        start_date: 開始日（YYYYMMDD形式の文字列、またはdatetimeオブジェクト）
        end_date: 終了日（YYYYMMDD形式の文字列、またはdatetimeオブジェクト）
        max_results: 最大結果数（デフォルトは10）
    
    Returns:
        検索結果のリスト
    """
    # 日付範囲のクエリを構築
    date_query = ""
    
    if start_date or end_date:
        # 日付をYYYYMMDD形式に変換
        if isinstance(start_date, datetime):
            start_str = start_date.strftime('%Y%m%d')
        elif start_date:
            start_str = str(start_date).replace('-', '')
        else:
            start_str = None
            
        if isinstance(end_date, datetime):
            end_str = end_date.strftime('%Y%m%d')
        elif end_date:
            end_str = str(end_date).replace('-', '')
        else:
            end_str = None
        
        # 日付範囲のクエリを構築
        if start_str and end_str:
            date_query = f'submittedDate:[{start_str} TO {end_str}]'
        elif start_str:
            date_query = f'submittedDate:[{start_str} TO *]'
        elif end_str:
            date_query = f'submittedDate:[* TO {end_str}]'
    else:
        date_query = '*'
    
    # 検索を実行
    client = arxiv.Client()
    search = arxiv.Search(
        query=date_query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    
    # 検索結果をリストに変換
    results = list(client.results(search))
    return results


if __name__ == "__main__":
    # ===== 検索パラメータ =====
    # 日付設定
    target_date = "20240923"  # 検索開始日
    end_target = "20241023"   # 検索終了日
    max_results = 100   # 最大結果数
    
    # ===== 検索実行 =====
    results = search_papers_by_date(
        start_date=target_date,
        end_date=end_target,
        max_results=max_results
    )

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