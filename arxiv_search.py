"""
arXiv論文検索モジュール
"""
import arxiv
from datetime import datetime
from typing import Optional, List, Union


def _format_date_to_yyyymmdd(date: Union[str, datetime, None]) -> Optional[str]:
    """
    日付をYYYYMMDD形式の文字列に変換する
    
    Args:
        date: 日付（YYYYMMDD形式の文字列、datetimeオブジェクト、またはNone）
    
    Returns:
        YYYYMMDD形式の文字列、またはNone
    """
    if date is None:
        return None
    
    if isinstance(date, datetime):
        return date.strftime('%Y%m%d')
    
    # 文字列の場合はハイフンを削除
    return str(date).replace('-', '')


def _build_date_query(start_date: Optional[str], end_date: Optional[str]) -> str:
    """
    日付範囲のクエリを構築する
    
    Args:
        start_date: 開始日（YYYYMMDD形式の文字列、またはNone）
        end_date: 終了日（YYYYMMDD形式の文字列、またはNone）
    
    Returns:
        arXiv検索用の日付クエリ文字列
    """
    if start_date and end_date:
        return f'submittedDate:[{start_date} TO {end_date}]'
    elif start_date:
        return f'submittedDate:[{start_date} TO *]'
    elif end_date:
        return f'submittedDate:[* TO {end_date}]'
    else:
        return '*'


def search_papers_by_date(
    start_date: Optional[Union[str, datetime]] = None,
    end_date: Optional[Union[str, datetime]] = None,
    max_results: int = 10
) -> List[arxiv.Result]:
    """
    特定の日付範囲でarXiv論文を検索する関数
    
    Args:
        start_date: 開始日（YYYYMMDD形式の文字列、またはdatetimeオブジェクト）
        end_date: 終了日（YYYYMMDD形式の文字列、またはdatetimeオブジェクト）
        max_results: 最大結果数（デフォルトは10）
    
    Returns:
        検索結果のリスト
    """
    # 日付をYYYYMMDD形式に変換
    start_str = _format_date_to_yyyymmdd(start_date)
    end_str = _format_date_to_yyyymmdd(end_date)
    
    # 日付範囲のクエリを構築
    date_query = _build_date_query(start_str, end_str)
    
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

