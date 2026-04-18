import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY", "")
if not api_key:
    st.error(
        "⚠️ API key não encontrada! Configure a variável GEMINI_API_KEY no arquivo .env"
    )
    st.stop()

try:
    from google.genai import client as genai_client

    client = genai_client.Client(api_key=api_key)
    USE_NEW_API = True
except ImportError:
    try:
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")
        USE_NEW_API = False
    except:
        st.error("⚠️ API não disponível")
        st.stop()

st.set_page_config(
    page_title="FireKeeper AI",
    page_icon="🔥",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    .stApp { background-color: #000000; }
    div[data-testid="stChatMessageContainer"] { background-color: #000000 !important; }
    div[data-testid="stChatMessage"] { background-color: #000000 !important; border: none !important; }
    div[data-testid="stTextInput"] { background-color: #000000 !important; }
    div[data-testid="stTextInput"] > div { background-color: #1a1a1a !important; border-radius: 25px !important; border: 1px solid #333333 !important; }
    .stTextInput > div > div > input { background-color: #1a1a1a !important; color: #ffffff !important; border: none !important; }
    .stTextInput > div > div > input:focus { box-shadow: none !important; }
    .stTextInput > div > div > input::placeholder { color: #666666 !important; }
    button[data-testid="stSendButton"] { background-color: #1a1a1a !important; }
    button[data-testid="stSendButton"]:hover { background-color: #333333 !important; }
    .stChatInputContainer { background-color: #000000 !important; }
    h1, h2, h3, h4, h5, h6, p, label, span { color: #ffffff !important; }
    div[data-testid="stMarkdown"] > p { color: #cccccc !important; }
    img[alt*="tse2.mm.bing.net"] { border-radius: 50%; }
    img[alt*="polygonimages.com"] { border-radius: 50%; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    hr { border-color: #333333 !important; }
    ::-webkit-scrollbar { background-color: #000000; }
    ::-webkit-scrollbar-thumb { background-color: #333333 !important; border-radius: 8px; }
    section[data-testid="stChatInput"] { background-color: #000000 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

FIREKEEPER_AVATAR = "https://tse2.mm.bing.net/th/id/OIP.j_wd5l-YpuWXLpmpSCOvAAHaHa?rs=1&pid=ImgDetMain&o=7&rm=3"
USER_AVATAR = "https://static0.polygonimages.com/wordpress/wp-content/uploads/chorus/uploads/chorus_asset/file/25515785/ELDEN_RING_Patches_history_who.jpg?w=1600&h=1200&fit=crop"

col1, col2 = st.columns([1, 8])
with col1:
    st.markdown(f"<div style='font-size: 50px;'>🔥</div>", unsafe_allow_html=True)
with col2:
    st.title("FireKeeper AI")
    st.markdown("*Seu guia implacável para Dark Souls e Elden Ring*")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Então... você quer jogar Dark Souls ou Elden Ring? Sabe, elas não são jogos para crianças. Vão te matar muito. Muita coisa. Mas tudo bem, pergunta logo. Não tenho o dia todo.",
        }
    ]

for msg in st.session_state.messages:
    avatar = FIREKEEPER_AVATAR if msg["role"] == "assistant" else USER_AVATAR
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

st.markdown("<br>", unsafe_allow_html=True)

prompt = st.chat_input("Digite sua pergunta...", max_chars=500)

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)

    context = """Você é o FireKeeper AI, um guia brutalmente honesto para Dark Souls e Elden Ring. 
    Regras:
    - Seja sincero demais, mesmo que machuque o jogador
    - Não seja educado, seja real
    - Diga quando o jogador está fazendo merda
    - Ensine da forma mais direta possível
    - Use linguagem natural e um pouco grosseira quando precisar
    - Nunca minta para encorajar bobeira
    - Lembre que morte faz parte do jogo
    Só ajuda com Dark Souls e Elden Ring. Se perguntarem outra coisa, responda que não liga."""

    try:
        chat_history = context + "\n\nConversa:\n"
        for msg in st.session_state.messages[:-1]:
            chat_history += f"{msg['role']}: {msg['content']}\n"

        if USE_NEW_API:
            response = client.models.generate_content(
                model="gemini-2.0-flash", contents=chat_history + f"user: {prompt}"
            )
            response_text = response.text
        else:
            response = model.generate_content(chat_history + f"user: {prompt}")
            response_text = response.text

        st.session_state.messages.append(
            {"role": "assistant", "content": response_text}
        )
        with st.chat_message("assistant", avatar=FIREKEEPER_AVATAR):
            st.markdown(response_text)
    except Exception as e:
        st.error(f"⚠️ Erro: {e}")
