"""
arXiv論文検索Webアプリケーション（Streamlit）
"""
import streamlit as st
from datetime import datetime, timedelta
from typing import Optional, List
import arxiv

from arxiv_search import search_papers_by_date
from date_utils import get_date_range, DATE_MODE_AUTO, DATE_MODE_MANUAL
from gemini_module import classify_genre
from main import format_author_list, format_category_list, classify_paper_genre


# ページ設定
st.set_page_config(
    page_title="arXiv論文検索アプリ",
    page_icon="📚",
    layout="wide"
)

# タイトル
st.title("📚 arXiv論文検索アプリ")
st.markdown("arXivから論文を検索し、Gemini APIでジャンル分類を行います。")

# サイドバー: 検索設定
with st.sidebar:
    st.header("🔍 検索設定")
    
    # 日付モード選択
    date_mode = st.radio(
        "日付モード",
        [DATE_MODE_AUTO, DATE_MODE_MANUAL],
        format_func=lambda x: "自動（前日）" if x == DATE_MODE_AUTO else "手動指定"
    )
    
    # 日付設定
    if date_mode == DATE_MODE_MANUAL:
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(
                "開始日",
                value=datetime.now() - timedelta(days=30),
                max_value=datetime.now()
            )
        with col2:
            end_date = st.date_input(
                "終了日",
                value=datetime.now(),
                max_value=datetime.now()
            )
        
        # 日付をYYYYMMDD形式に変換
        manual_start_date = start_date.strftime('%Y%m%d')
        manual_end_date = end_date.strftime('%Y%m%d')
    else:
        manual_start_date = None
        manual_end_date = None
    
    # 最大結果数
    max_results = st.slider(
        "最大結果数",
        min_value=1,
        max_value=100,
        value=10,
        step=1
    )
    
    st.divider()
    
    # Gemini判定設定
    st.header("🤖 Gemini判定設定")
    enable_gemini = st.checkbox("Gemini判定を有効にする", value=True)
    
    if enable_gemini:
        target_genre = st.text_input(
            "判定したいジャンル",
            value="自動運転",
            placeholder="例: 自動運転、機械学習、自然言語処理"
        )
    else:
        target_genre = None

# メインエリア
# 検索ボタン
if st.button("🔍 検索実行", type="primary", use_container_width=True):
    with st.spinner("論文を検索中..."):
        try:
            # 日付範囲の取得
            if date_mode == DATE_MODE_AUTO:
                target_date, end_target = get_date_range(mode=DATE_MODE_AUTO)
            else:
                target_date, end_target = get_date_range(
                    mode=DATE_MODE_MANUAL,
                    start_date=manual_start_date,
                    end_date=manual_end_date
                )
            
            # 検索実行
            results = search_papers_by_date(
                start_date=target_date,
                end_date=end_target,
                max_results=max_results
            )
            
            # 結果をセッション状態に保存
            st.session_state['results'] = results
            st.session_state['target_genre'] = target_genre if enable_gemini else None
            st.session_state['enable_gemini'] = enable_gemini
            
            st.success(f"検索完了: {len(results)}件の論文が見つかりました")
            
        except Exception as e:
            st.error(f"エラーが発生しました: {str(e)}")
            st.session_state['results'] = []

# 検索結果の表示
if 'results' in st.session_state and st.session_state['results']:
    results = st.session_state['results']
    target_genre = st.session_state.get('target_genre')
    enable_gemini = st.session_state.get('enable_gemini', False)
    
    st.header(f"📄 検索結果 ({len(results)}件)")
    
    # 検索条件の表示
    with st.expander("検索条件を表示"):
        if date_mode == DATE_MODE_AUTO:
            st.write(f"**日付モード**: 自動（前日）")
        else:
            st.write(f"**開始日**: {start_date.strftime('%Y年%m月%d日')}")
            st.write(f"**終了日**: {end_date.strftime('%Y年%m月%d日')}")
        st.write(f"**最大結果数**: {max_results}")
        if enable_gemini and target_genre:
            st.write(f"**Gemini判定ジャンル**: {target_genre}")
    
    # 結果を表示
    for i, result in enumerate(results, 1):
        with st.container():
            # タイトル
            st.subheader(f"{i}. {result.title}")
            
            # メタ情報
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**著者**: {format_author_list(result.authors)}")
                st.write(f"**カテゴリー**: {format_category_list(result.categories)}")
            
            with col2:
                st.write(f"**公開日**: {result.published.strftime('%Y年%m月%d日') if result.published else '不明'}")
                st.markdown(f"[論文リンク]({result.entry_id})", unsafe_allow_html=True)
            
            # アブストラクト
            if result.summary:
                with st.expander("📝 アブストラクトを表示"):
                    st.write(result.summary)
            
            # Gemini判定
            if enable_gemini and target_genre and result.summary:
                with st.spinner(f"Gemini判定中（{target_genre}）..."):
                    classification = classify_paper_genre(target_genre, result.summary)
                    if classification:
                        # 判定結果に応じて色分け
                        if classification.strip().upper() == "YES":
                            st.success(f"✅ **Gemini判定（{target_genre}）**: {classification}")
                        else:
                            st.info(f"❌ **Gemini判定（{target_genre}）**: {classification}")
            
            st.divider()
    
    # 結果の統計
    if enable_gemini and target_genre:
        st.subheader("📊 判定結果の統計")
        yes_count = 0
        no_count = 0
        
        for result in results:
            if result.summary:
                classification = classify_paper_genre(target_genre, result.summary)
                if classification:
                    if classification.strip().upper() == "YES":
                        yes_count += 1
                    else:
                        no_count += 1
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("該当する論文", yes_count)
        with col2:
            st.metric("該当しない論文", no_count)

elif 'results' in st.session_state and len(st.session_state['results']) == 0:
    st.info("検索結果がありませんでした。検索条件を変更して再度お試しください。")

else:
    st.info("👈 左側のサイドバーで検索条件を設定し、「検索実行」ボタンをクリックしてください。")

# フッター
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "arXiv論文検索アプリ | Powered by Streamlit"
    "</div>",
    unsafe_allow_html=True
)

