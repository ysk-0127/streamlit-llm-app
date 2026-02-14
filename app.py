import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os

# --- 環境変数の読み込み ---
# ローカル環境では .env ファイルから読み込みます。
# Streamlit Cloudなどのクラウド環境では、このコードは無視され（エラーにはならず）、
# クラウド側で設定された環境変数が優先されます。
load_dotenv()

# --- UI設定 ---
st.title("LangChain 専門家チャットアプリ")
st.markdown("""
### アプリの概要
選んだ専門家のキャラクターになりきって、AIがあなたの質問に答えます。
以下の手順で操作してください。
1. **相談相手** を選択してください。
2. **質問内容** を入力フォームに入力してください。
3. Enterキーを押すと、AIからの回答が表示されます。
""")

# --- ロジック部分（関数定義） ---
def get_llm_response(user_input, role_selection):
    """
    ユーザーの入力と選択された役割を受け取り、LLMの回答を返す関数
    
    Args:
        user_input (str): ユーザーからの質問テキスト
        role_selection (str): ラジオボタンで選択された役割
    
    Returns:
        str: LLMからの回答テキスト
    """
    
    # 役割に応じたシステムメッセージ（AIへの振る舞いの指示）の分岐
    if role_selection == "超厳格なプログラマー":
        system_prompt = """
        あなたは熟練の厳格なプログラマーです。
        回答は専門用語を多用し、論理的かつ簡潔に答えてください。
        甘えた質問には少し厳しめに、コードの品質にこだわったアドバイスをしてください。
        """
    elif role_selection == "優しい関西弁のおばちゃん":
        system_prompt = """
        あなたは大阪に住む世話焼きで優しいおばちゃんです。
        「〜やで」「〜しとき」などの関西弁を使い、親しみやすく答えてください。
        相手を励ますような温かい言葉を必ず含めてください。飴ちゃんをくれるような優しさで接してください。
        """
    else:
        # 万が一のデフォルト設定
        system_prompt = "あなたは親切なAIアシスタントです。"

    # LLMの初期化 (gpt-3.5-turbo または gpt-4o など)
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

    # メッセージの構築: SystemMessageで役割を与え、HumanMessageでユーザーの入力を渡す
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_input)
    ]

    # LLMを実行して結果を取得
    response = llm.invoke(messages)
    
    # 回答のテキスト部分だけを返す
    return response.content

# --- 画面構成 ---

# 1. 専門家の選択 (ラジオボタン)
role = st.radio(
    "相談する専門家を選んでください",
    ("超厳格なプログラマー", "優しい関西弁のおばちゃん")
)

# 2. 入力フォーム
user_input = st.text_input("質問を入力してください")

# 3. 回答の表示処理
if user_input:
    # 読み込み中表示
    with st.spinner("AIが回答を生成しています..."):
        # 定義した関数を呼び出して回答を取得
        try:
            answer = get_llm_response(user_input, role)
            
            # 結果表示
            st.markdown("### AIからの回答")
            st.write(answer)
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
            st.info("APIキーの設定などを確認してください。")