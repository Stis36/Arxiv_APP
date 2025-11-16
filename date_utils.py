"""
日付設定ユーティリティモジュール
"""
from datetime import datetime, timedelta


def get_date_range(mode="auto", start_date=None, end_date=None):
    """
    日付範囲を取得する関数
    
    Args:
        mode: "auto" (前日を自動計算) または "manual" (手動で日付を指定)
        start_date: 手動モード時の開始日（YYYYMMDD形式の文字列）
        end_date: 手動モード時の終了日（YYYYMMDD形式の文字列）
    
    Returns:
        (start_date, end_date) のタプル（YYYYMMDD形式の文字列）
    """
    if mode == "auto":
        # 前日を自動計算
        yesterday = datetime.now() - timedelta(days=1)
        target_date = yesterday.strftime('%Y%m%d')
        end_target = yesterday.strftime('%Y%m%d')
        return target_date, end_target
    else:
        # 手動で日付を指定
        if start_date is None or end_date is None:
            raise ValueError("manualモードではstart_dateとend_dateの両方を指定してください")
        return start_date, end_date

