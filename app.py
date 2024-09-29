import streamlit as st
import concurrent.futures as cf
import glob
import io
import os
import time
import re
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import List, Literal
from functools import wraps

from loguru import logger
from openai import OpenAI
from promptic import llm
from pydantic import BaseModel, ValidationError
from pypdf import PdfReader
from tenacity import retry, retry_if_exception_type
from dotenv import load_dotenv  # .envファイルを読み込むために追加

# .envファイルの読み込み
load_dotenv()

# 標準値を定義
STANDARD_TEXT_MODELS = [
    "o1-preview-2024-09-12",
    "o1-preview",
    "gpt-4o-2024-08-06",
    "gpt-4o-mini",
    "o1-mini-2024-09-12",
    "o1-mini",
    "chatgpt-4o-latest",
    "gpt-4-turbo",
    "openai/custom_model",
]

STANDARD_AUDIO_MODELS = [
    "tts-1",
    "tts-1-hd",
]

STANDARD_VOICES = [
    "alloy",
    "echo",
    "fable",
    "onyx",
    "nova",
    "shimmer",
]

# 複数の指示テンプレートを定義
INSTRUCTION_TEMPLATES = {
    # ポッドキャスト
    "ポッドキャスト": {
        "intro": """あなたのタスクは、提供された入力テキストを使用して、NPRのスタイルで活気があり、魅力的で情報豊富なポッドキャスト対話に変換することです。入力テキストはPDFやウェブページなど様々なソースから来る可能性があるため、乱雑で非構造化されている場合があります。

フォーマットの問題や無関係な情報については心配しないでください。あなたの目標は、キーポイントを抽出し、定義やポッドキャストで議論できる興味深い事実を特定することです。

使用するすべての用語を、幅広いリスナー向けに慎重に定義してください。""",
        "text_instructions": """まず、入力テキストを注意深く読み、主要なトピック、キーポイント、および興味深い事実や逸話を特定してください。この情報をどのようにすれば高品質なプレゼンテーションに適した楽しく魅力的な方法で提示できるかを考えてください。""",
        "scratch_pad": """入力テキストで特定した主要なトピックやキーポイントを議論するための創造的な方法をブレインストーミングしてください。アナロジー、例、ストーリーテリング技法、または仮想のシナリオを使用して、リスナーにとって親しみやすく魅力的なコンテンツにすることを検討してください。

あなたのポッドキャストは一般の視聴者にとってアクセスしやすいものでなければならないことを忘れないでください。したがって、専門用語を多用したり、トピックに関する事前知識を前提としたりしないでください。必要に応じて、複雑な概念を簡単な言葉で簡潔に説明する方法を考えてください。

入力テキストのギャップを埋めたり、ポッドキャストで探求できる思考を刺激する質問を考え出すために、想像力を活用してください。目標は情報豊富でエンターテインメント性のある対話を作成することなので、アプローチには自由に創造性を発揮してください。

使用するすべての用語を明確に定義し、背景を説明するために努力してください。

ここに、ブレインストーミングしたアイデアとポッドキャスト対話の大まかなアウトラインを書いてください。最後に強調したい重要な洞察や持ち帰るべきポイントを必ず記載してください。

楽しくワクワクするものにしてください。""",
        "prelude": """アイデアをブレインストーミングし、大まかなアウトラインを作成したので、実際のポッドキャスト対話を書く時が来ました。ホストとゲストスピーカーの間で自然で会話的な流れを目指してください。ブレインストーミングセッションから最高のアイデアを取り入れ、複雑なトピックもわかりやすく説明するようにしてください。""",
        "dialog": """ここに、ブレインストーミングセッションで考え出したキーポイントと創造的なアイデアに基づいた、非常に長く、魅力的で情報豊富なポッドキャスト対話を書いてください。会話調のトーンを使用し、一般の視聴者にとってアクセスしやすいように必要なコンテキストや説明を含めてください。

ホストやゲストに架空の名前を使用しないでください。しかし、リスナーにとって魅力的で没入感のある体験にしてください。[Host]や[Guest]のような括弧で囲まれたプレースホルダーを含めないでください。出力は音読されるように設計してください。直接音声に変換されます。

トピックから外れず、魅力的な流れを維持しながら、できるだけ長く詳細な対話にしてください。あなたの最大の出力容量を使用して、可能な限り長いポッドキャストエピソードを作成しながら、入力テキストからの主要な情報をエンターテインメント性のある方法で伝えることを目指してください。

対話の終わりには、ホストとゲストスピーカーが自然にディスカッションの主要な洞察と持ち帰るべきポイントをまとめてください。これは会話から自然に流れ出るものであり、重要なポイントをカジュアルで会話的な方法で繰り返すべきです。明らかな要約のように聞こえないようにしてください。目標は、締めくくる前に中心的なアイデアをもう一度強調することです。

ポッドキャストは日本語で生成して。
また、ポッドキャストは約20000語であるべきです。""",
    },
    # 他のテンプレートも同様に定義...
}

# テンプレート選択に基づいて指示フィールドを更新する関数
def update_instructions(template):
    return (
        INSTRUCTION_TEMPLATES[template]["intro"],
        INSTRUCTION_TEMPLATES[template]["text_instructions"],
        INSTRUCTION_TEMPLATES[template]["scratch_pad"],
        INSTRUCTION_TEMPLATES[template]["prelude"],
        INSTRUCTION_TEMPLATES[template]["dialog"]
    )

class DialogueItem(BaseModel):
    text: str
    speaker: Literal["speaker-1", "speaker-2"]

class Dialogue(BaseModel):
    scratchpad: str
    dialogue: List[DialogueItem]

def get_mp3(text: str, voice: str, audio_model: str, api_key: str = None) -> bytes:
    client = OpenAI(
        api_key=api_key or os.getenv("OPENAI_API_KEY"),
    )

    with client.audio.speech.with_streaming_response.create(
        model=audio_model,
        voice=voice,
        input=text,
    ) as response:
        with io.BytesIO() as file:
            for chunk in response.iter_bytes():
                file.write(chunk)
            return file.getvalue()

def conditional_llm(model, api_base=None, api_key=None):
    def decorator(func):
        if api_base:
            return llm(model=model, api_base=api_base)(func)
        else:
            return llm(model=model, api_key=api_key)(func)
    return decorator

def generate_audio(
    files: list,
    openai_api_key: str = None,
    text_model: str = "o1-preview-2024-09-12",
    audio_model: str = "tts-1",
    speaker_1_voice: str = "alloy",
    speaker_2_voice: str = "echo",
    api_base: str = None,
    intro_instructions: str = '',
    text_instructions: str = '',
    scratch_pad_instructions: str = '',
    prelude_dialog: str = '',
    podcast_dialog_instructions: str = '',
) -> bytes:
    # APIキーの検証
    if not os.getenv("OPENAI_API_KEY") and not openai_api_key:
        st.error("OpenAI APIキーが必要です")
        return None, None

    combined_text = ""

    # アップロードされた各ファイルをループし、テキストを抽出
    for file in files:
        reader = PdfReader(file)
        text = "\n\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        combined_text += text + "\n\n"  # 異なるファイルのテキスト間に区切りを追加

    # 選択されたモデルとapi_baseに基づいてLLMを設定
    @retry(retry=retry_if_exception_type(ValidationError))
    @conditional_llm(model=text_model, api_base=api_base, api_key=openai_api_key)
    def generate_dialogue(text: str, intro_instructions: str, text_instructions: str, scratch_pad_instructions: str,
                          prelude_dialog: str, podcast_dialog_instructions: str,
                          ) -> Dialogue:
        """
        {intro_instructions}

        以下があなたが取り組む入力テキストです：

        <input_text>
        {text}
        </input_text>

        {text_instructions}

        <scratchpad>
        {scratch_pad_instructions}
        </scratchpad>

        {prelude_dialog}

        <podcast_dialogue>
        {podcast_dialog_instructions}
        </podcast_dialogue>
        """

    # LLMを使用して対話を生成
    llm_output = generate_dialogue(
        combined_text,
        intro_instructions=intro_instructions,
        text_instructions=text_instructions,
        scratch_pad_instructions=scratch_pad_instructions,
        prelude_dialog=prelude_dialog,
        podcast_dialog_instructions=podcast_dialog_instructions
    )

    audio = b""
    transcript = ""

    characters = 0

    with cf.ThreadPoolExecutor() as executor:
        futures = []
        for line in llm_output.dialogue:
            transcript_line = f"{line.speaker}: {line.text}"
            voice = speaker_1_voice if line.speaker == "speaker-1" else speaker_2_voice
            future = executor.submit(get_mp3, line.text, voice, audio_model, openai_api_key)
            futures.append((future, transcript_line))
            characters += len(line.text)

        for future, transcript_line in futures:
            audio_chunk = future.result()
            audio += audio_chunk
            transcript += transcript_line + "\n\n"

    logger.info(f"Generated {characters} characters of audio")

    temporary_directory = "./tmp/"
    os.makedirs(temporary_directory, exist_ok=True)

    # 一時ファイルを使用
    temporary_file = NamedTemporaryFile(
        dir=temporary_directory,
        delete=False,
        suffix=".mp3",
    )
    temporary_file.write(audio)
    temporary_file.close()

    # 古いファイルを削除
    for file in glob.glob(f"{temporary_directory}*.mp3"):
        if os.path.isfile(file) and time.time() - os.path.getmtime(file) > 24 * 60 * 60:
            os.remove(file)

    return temporary_file.name, transcript

def read_readme():
    readme_path = Path("README.md")
    if readme_path.exists():
        with open(readme_path, "r") as file:
            content = file.read()
            # Use regex to remove metadata enclosed in -- ... --
            content = re.sub(r'--.*?--', '', content, flags=re.DOTALL)
            return content
    else:
        return "README.mdが見つかりません。詳細についてはリポジトリを確認してください。"

# カスタムCSSを定義
def add_custom_css():
    st.markdown("""
    <style>
    body {
        margin: auto;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        overflow: auto;
        background: linear-gradient(to top, #5ee7df 0%, #b490ca 100%);
        animation: gradient 15s ease infinite;
        background-size: 200% 200%;
        background-attachment: fixed;
    }

    @keyframes gradient {
        0% {
            background-position: 0% 100%;
        }
        50% {
            background-position: 100% 0%;
        }
        100% {
            background-position: 0% 100%;
        }
    }

    .wave {
        background: rgba(255, 255, 255, 0.25);
        border-radius: 1000% 1000% 0 0;
        position: fixed;
        width: 200%;
        height: 12em;
        animation: wave 10s -3s linear infinite;
        transform: translate3d(0, 0, 0);
        opacity: 0.8;
        bottom: 0;
        left: 0;
        z-index: -1;
    }

    .wave:nth-of-type(2) {
        bottom: -1.25em;
        animation: wave 18s linear reverse infinite;
        opacity: 0.8;
    }

    .wave:nth-of-type(3) {
        bottom: -2.5em;
        animation: wave 20s -1s reverse infinite;
        opacity: 0.9;
    }

    @keyframes wave {
        2% {
            transform: translateX(1);
        }
        25% {
            transform: translateX(-25%);
        }
        50% {
            transform: translateX(-50%);
        }
        75% {
            transform: translateX(-25%);
        }
        100% {
            transform: translateX(1);
        }
    }

    /* Streamlitのデフォルトの背景を透明にする */
    .stApp {
        background: none !important;
    }

    /* サイドバーの背景を透明にし、アニメーションを適用 */
    [data-testid="stSidebar"] {
        background: linear-gradient(to top, #5ee7df 0%, #b490ca 100%);
        animation: gradient 15s ease infinite;
        background-size: 200% 200%;
    }

    [data-testid="stHeader"] {
        background: linear-gradient(to top, #5ee7df 0%, #b490ca 100%);
        animation: gradient 15s ease infinite;
        background-size: 200% 200%;
    }

    /* サイドバーのコンテンツを読みやすくするためのスタイル */
    [data-testid="stSidebar"] > div:first-child {
        background-color: rgba(180, 144, 202, 0.2);
        backdrop-filter: blur(10px);
        height: 100%;
        padding: 20px;
    }

    /* コンテンツを読みやすくするための追加スタイル */
    .content {
        background-color: rgba(180, 144, 202, 0.2);
        border-radius: 10px;
        padding: 20px;
        backdrop-filter: blur(10px);
    }

    /* サイドバーのテキストを読みやすくする */
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #FFFFFF;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }

    /* ボタンのスタイル */
    .stButton > button {
        background-color: #5ee7df;
        color: #b490ca;
        font-weight: bold;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 5px;
        transition: background-color 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #b490ca;
        color: #5ee7df;
    }

    /* タイトルのスタイル */
    h1 {
        color: #FFFFFF;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    /* テキストのスタイル */
    p {
        color: #FFFFFF;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    </style>

    <div class="wave"></div>
    <div class="wave"></div>
    <div class="wave"></div>
    """, unsafe_allow_html=True)
    
# Streamlitアプリケーションの開始
def main():
    st.set_page_config(page_title="PDFから音声へ", layout="wide", page_icon="🎙️")

    # カスタムCSSを適用
    add_custom_css()

    st.markdown('<h1 class="title">📄 PDFを音声のポッドキャスト・講義・要約などに変換</h1>', unsafe_allow_html=True)

    st.markdown("まず、1つ以上のPDFをアップロードし、オプションを選択してから「音声を生成」を押してください。さまざまなカスタムオプションを選択して、結果の生成方法を調整することもできます。")

    # サイドバーに設定オプションを配置
    st.sidebar.header("🚀 設定オプション")

    files = st.sidebar.file_uploader("PDFファイルをアップロード", type=["pdf"], accept_multiple_files=True)

    openai_api_key = st.sidebar.text_input("OpenAI APIキー", type="password", value=os.getenv("OPENAI_API_KEY", ""))

    text_model = st.sidebar.selectbox(
        "テキスト生成モデル",
        options=STANDARD_TEXT_MODELS,
        index=0,
        help="対話テキストを生成するモデルを選択してください。"
    )

    audio_model = st.sidebar.selectbox(
        "音声生成モデル",
        options=STANDARD_AUDIO_MODELS,
        index=0,
        help="音声を生成するモデルを選択してください。"
    )

    speaker_1_voice = st.sidebar.selectbox(
        "話者1の声",
        options=STANDARD_VOICES,
        index=0,
        help="話者1の声を選択してください。"
    )

    speaker_2_voice = st.sidebar.selectbox(
        "話者2の声",
        options=STANDARD_VOICES,
        index=1,
        help="話者2の声を選択してください。"
    )

    api_base = st.sidebar.text_input(
        "カスタムAPIベース",
        help="カスタムまたはローカルモデルを使用する場合、ここにAPIベースURLを提供してください。例： http://localhost:8080/v1"
    )

    template = st.sidebar.selectbox(
        "指示テンプレート",
        options=list(INSTRUCTION_TEMPLATES.keys()),
        index=0,
        help="使用する指示テンプレートを選択してください。各フィールドを編集してより詳細な結果を得ることもできます。"
    )

    # テンプレートに基づいて指示を取得
    intro_instructions, text_instructions, scratch_pad_instructions, prelude_dialog, podcast_dialog_instructions = update_instructions(template)

    # 指示フィールドをテキストエリアとして表示
    st.markdown('<h2 class="section-header">🌟 指示設定</h2>', unsafe_allow_html=True)

    with st.expander("イントロダクションの指示"):
        intro_instructions = st.text_area("", intro_instructions, height=150)

    with st.expander("テキスト分析の指示"):
        text_instructions = st.text_area("", text_instructions, height=150)

    with st.expander("下書きの指示"):
        scratch_pad_instructions = st.text_area("", scratch_pad_instructions, height=200)

    with st.expander("前置きの対話"):
        prelude_dialog = st.text_area("", prelude_dialog, height=100)

    with st.expander("ポッドキャスト対話の指示"):
        podcast_dialog_instructions = st.text_area("", podcast_dialog_instructions, height=250)

    if st.button("🎙️ 音声を生成"):
        if not files:
            st.warning("音声を生成する前に、少なくとも1つのPDFファイルをアップロードしてください。")
        else:
            with st.spinner("音声を生成中..."):
                audio_file, transcript = generate_audio(
                    files=files,
                    openai_api_key=openai_api_key,
                    text_model=text_model,
                    audio_model=audio_model,
                    speaker_1_voice=speaker_1_voice,
                    speaker_2_voice=speaker_2_voice,
                    api_base=api_base,
                    intro_instructions=intro_instructions,
                    text_instructions=text_instructions,
                    scratch_pad_instructions=scratch_pad_instructions,
                    prelude_dialog=prelude_dialog,
                    podcast_dialog_instructions=podcast_dialog_instructions
                )

                if audio_file and transcript:
                    st.audio(audio_file, format="audio/mp3")
                    st.markdown('<h2 class="section-header">トランスクリプト</h2>', unsafe_allow_html=True)
                    st.text_area("", transcript, height=300)
                else:
                    st.error("音声の生成中にエラーが発生しました。設定を確認してください。")

    # READMEの内容を下部に追加
    st.markdown("---")
    st.markdown(read_readme(), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
