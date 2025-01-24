import os
import streamlit as st
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv

# 環境変数の読み込み（Streamlitコマンドより前ならOK）
load_dotenv()

# Geminiの設定（Streamlitコマンドより前ならOK）
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")


def analyze_image(image, prompt):
    """画像分析とキャプション生成"""
    try:
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")
        return None


def process_image(uploaded_file):
    """画像処理"""
    return Image.open(uploaded_file)


# プロンプトテンプレート
PROMPT_TEMPLATE = """
あなたはプロのSNSコンサルタントです。以下の商品画像からInstagram向けのキャプションを3案生成してください。

【要件】
- 商品の視覚的特徴を活かす
- 各案は最大200文字
- ハッシュタグを3つ追加
- 親しみやすい口調
- 絵文字を適度に使用
- 行動を促すフレーズを含む

【出力形式】
1. [キャプション案1] 
   - ハッシュタグ: #xxx #yyy #zzz
2. [キャプション案2]
   - ハッシュタグ: #aaa #bbb #ccc
3. [キャプション案3]
   - ハッシュタグ: #ddd #eee #fff
"""


def main():
    # 最初にページ設定を実行
    st.set_page_config(page_title="SNSキャプション生成", layout="centered", page_icon="📸")

    # カスタムCSSスタイル
    st.markdown(
        """
    <style>
    /* ボタンアニメーション */
    .stButton>button {
        transition: all 0.3s ease;
        border-radius: 8px !important;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    /* ヘッダー装飾 */
    h1 {
        color: #FF6B6B !important;
        text-align: center;
        margin-bottom: 30px !important;
    }

    /* ローディングスピナー */
    .stSpinner > div {
        border-color: #FF6B6B transparent transparent transparent !important;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # セッション状態の初期化
    session_defaults = {
        "generated": False,
        "response": None,
        "uploaded_file": None,
        "history": [],
        "copied": None,
    }

    for key, value in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    st.title("📸 商品キャプション生成アプリ")

    # サイドバーに履歴表示
    with st.sidebar:
        st.subheader("生成履歴")
        if st.session_state.history:
            for idx, item in enumerate(st.session_state.history[::-1]):
                with st.expander(f"履歴 {len(st.session_state.history)-idx}"):
                    st.image(item["image"], use_column_width=True)
                    st.write(item["caption"])
        else:
            st.write("履歴がありません")

    if not st.session_state.generated:
        # メイン画面（画像アップロード）
        uploaded_file = st.file_uploader(
            "商品画像をアップロード", type=["jpg", "png"], help="JPEGまたはPNG形式の画像を選択してください"
        )

        if uploaded_file is not None:
            col1, col2 = st.columns(2)
            with col1:
                st.image(uploaded_file, caption="アップロード画像", use_container_width=True)

            if st.button("✨ キャプションを生成", type="primary"):
                with st.spinner("画像を分析中..."):
                    image = process_image(uploaded_file)
                    response = analyze_image(image, PROMPT_TEMPLATE)

                    if response:
                        st.session_state.update(
                            {
                                "generated": True,
                                "response": response,
                                "uploaded_file": uploaded_file.getvalue(),
                                "history": st.session_state.history
                                + [{"image": uploaded_file.getvalue(), "caption": response}],
                            }
                        )
                        st.rerun()

    else:
        # 生成結果表示画面
        st.subheader("🎉 生成結果")

        col1, col2 = st.columns(2)
        with col1:
            st.image(st.session_state.uploaded_file, caption="アップロード画像", use_container_width=True)

        captions = [line for line in st.session_state.response.split("\n") if line.strip()]

        # キャプション表示
        for i, caption in enumerate(captions):
            with st.container(border=True):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"**案 {i+1}**\n\n{caption}")
                with col2:
                    if st.button("📋", key=f"copy_{i}", help="クリップボードにコピー"):
                        st.session_state.copied = caption
                        st.toast("クリップボードにコピーしました！", icon="✅")

        # アクションボタン群
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("🔄 再生成", help="同じ画像で再生成"):
                st.session_state.generated = False
                st.rerun()
        with col2:
            if st.button("📤 新規画像", help="別の画像をアップロード"):
                st.session_state.generated = False
                st.session_state.uploaded_file = None
                st.rerun()
        with col3:
            if st.button("📚 履歴表示", help="生成履歴を確認"):
                pass  # サイドバーに自動表示
        with col4:
            if st.button("🏠 最初に戻る", help="完全にリセット"):
                st.session_state.clear()
                st.rerun()


if __name__ == "__main__":
    main()
