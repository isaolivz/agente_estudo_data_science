import streamlit as st
from agente import AgenteInteligente
import os

st.set_page_config(
    page_title="Agente Inteligente",
    page_icon="robot",
    layout="wide"
)

st.title("Agente Inteligente")
st.markdown("Faca perguntas sobre seus documentos")

with st.sidebar:
    st.header("Documentos")
    if os.path.exists("./data"):
        docs = os.listdir("./data")
        for doc in docs:
            st.write(f"📄 {doc}")

@st.cache_resource
def carregar_agente():
    return AgenteInteligente()

try:
    agente = carregar_agente()
    if agente and agente.base.vector_store:
        st.success("Agente carregado com sucesso!")
    else:
        st.error("Nenhum documento encontrado")
        st.stop()
except Exception as e:
    st.error(f"Erro: {e}")
    st.stop()

pergunta = st.text_input("Digite sua pergunta:")

if st.button("Perguntar"):
    if pergunta:
        with st.spinner("Pensando..."):
            resposta = agente.perguntar(pergunta)
            st.markdown("### Resposta")
            st.write(resposta)
    else:
        st.warning("Digite uma pergunta")