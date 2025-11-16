"""
日付設定ユーティリティモジュール
"""
from datetime import datetime, timedelta
from typing import Tuple, Optional, Literal


# 定数定義
DATE_MODE_AUTO = "auto"
DATE_MODE_MANUAL = "manual"
DATE_FORMAT = "%Y%m%d"
DAYS_BACK = 1  # 前日を取得する場合の日数


def get_date_range(
    mode: Literal["auto", "manual"] = DATE_MODE_AUTO,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> Tuple[str, str]:
    """
    日付範囲を取得する関数
    
    Args:
        mode: "auto" (前日を自動計算) または "manual" (手動で日付を指定)
        start_date: 手動モード時の開始日（YYYYMMDD形式の文字列）
        end_date: 手動モード時の終了日（YYYYMMDD形式の文字列）
    
    Returns:
        (start_date, end_date) のタプル（YYYYMMDD形式の文字列）
    
    Raises:
        ValueError: manualモードでstart_dateまたはend_dateが指定されていない場合
    """
    if mode == DATE_MODE_AUTO:
        # 前日を自動計算
        yesterday = datetime.now() - timedelta(days=DAYS_BACK)
        date_str = yesterday.strftime(DATE_FORMAT)
        return date_str, date_str
    
    # 手動モード
    if start_date is None or end_date is None:
        raise ValueError(
            f"{DATE_MODE_MANUAL}モードではstart_dateとend_dateの両方を指定してください"
        )
    return start_date, end_date

