"""
arXiv論文検索モジュール
"""
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

