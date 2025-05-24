import streamlit as st
from openai import OpenAI
from bs4 import BeautifulSoup

# Configurações da página
st.set_page_config(page_title="Chatbot do Relatório", layout="wide")
st.title("💬 Chatbot do Relatório ENEM 2023")

# Testa leitura da chave
api_key = st.secrets["OPENAI_API_KEY"]

# Lê o HTML do relatório e extrai o texto
@st.cache_data
def carregar_html_como_texto(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator="\n").strip()

conteudo = carregar_html_como_texto("report_resultado_completo.html")

# Inicializa histórico da conversa
if "mensagens" not in st.session_state:
    st.session_state.mensagens = [
        {
            "role": "system",
            "content": (
                "Você é um assistente especializado neste relatório técnico.\n\n"
                "Responda apenas com base no conteúdo a seguir:\n\n" +
                conteudo +
                "\n\nSe não souber a resposta, diga que não sabe. "
                "Se a pergunta não estiver clara, peça para reformular. "
                "Se não for sobre o relatório, diga que não pode ajudar."
            )
        },
        {
            "role": "assistant",
            "content": "Olá! Estou aqui para responder perguntas sobre o relatório."
        }
    ]

# Exibe o histórico da conversa
for msg in st.session_state.mensagens[1:]:
    st.chat_message(msg["role"]).markdown(msg["content"])

# Entrada do usuário
pergunta = st.chat_input("Faça uma pergunta sobre o relatório...")

if pergunta:
    st.chat_message("user").markdown(pergunta)
    st.session_state.mensagens.append({"role": "user", "content": pergunta})

    client = OpenAI(api_key=api_key)
    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.mensagens
    )

    resposta_texto = resposta.choices[0].message.content
    st.chat_message("assistant").markdown(resposta_texto)
    st.session_state.mensagens.append({"role": "assistant", "content": resposta_texto})
