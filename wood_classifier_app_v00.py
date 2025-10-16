import openai
import streamlit as st
import base64

# --- Streamlit UI setup ---
st.set_page_config(page_title="木材分類器", layout="centered")
st.title("🌲 顕微鏡画像から木材を分類する（GPT-4o使用）")
st.markdown("""
以下の3種類のいずれかを判定します：
- アカマツ
- クリ
- クスノキ
""")

# --- Upload image ---
uploaded_file = st.file_uploader("顕微鏡画像をアップロードしてください", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="アップロード画像", use_column_width=True)
    img_bytes = uploaded_file.read()
    img_b64 = base64.b64encode(img_bytes).decode("utf-8")

    if st.button("分類する"):
        with st.spinner("GPT-4oが分類中です..."):
            openai.api_key = st.secrets["OPENAI_API_KEY"]

            # --- Few-shot messages with correct image_url type ---
            messages = [
                {
                    "role": "system",
                    "content": "あなたは木材顕微鏡画像の分類専門家です。分類対象はアカマツ、クリ、クスノキです。導管や樹脂道の特徴から判断してください。"
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "これはアカマツの木材顕微鏡画像です。"},
                        {"type": "image_url", "image_url": {"url": "https://i.imgur.com/ohpjN8s.jpeg"}}
                    ]
                },
                {
                    "role": "assistant",
                    "content": "この画像はアカマツです。大きな樹脂道があり、仮道管が整然と並んでいます。"
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "これはクスノキの木材顕微鏡画像です。"},
                        {"type": "image_url", "image_url": {"url": "https://i.imgur.com/2hFhidM.jpeg"}}
                    ]
                },
                {
                    "role": "assistant",
                    "content": "この画像はクスノキです。導管が散孔性で、ランダムに分布しています。"
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "これはクリの木材顕微鏡画像です。"},
                        {"type": "image_url", "image_url": {"url": "https://i.imgur.com/i0WYxt9.jpeg"}}
                    ]
                },
                {
                    "role": "assistant",
                    "content": "この画像はクリです。大きな導管が年輪に沿って整列しています。"
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "この画像はどの木材ですか？分類名と理由を教えてください。"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
                    ]
                }
            ]

            try:
                 # ChatCompletion呼び出し（v0系スタイル）
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=messages,
                )
                result = response.choices[0].message.content
                st.success("✅ 分類が完了しました")
                st.markdown("### 判定結果")
                st.write(result)

            except Exception as e:
                st.error("エラーが発生しました。APIキーや通信状況を確認してください。")
                st.exception(e)





