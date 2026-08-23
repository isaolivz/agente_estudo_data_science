import streamlit as st
from agente import AgenteInteligente
import os

# Configuração da página
st.set_page_config(
    page_title="Agente Inteligente - Data Science",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="expanded"
)

# CSS profissional
st.markdown("""
<style>
    /* Cabeçalho */
    .header {
        text-align: center;
        padding: 1.5rem 0 0.5rem 0;
        border-bottom: 2px solid #e6e9ef;
        margin-bottom: 1.5rem;
    }
    .header h1 {
        font-size: 2.2rem;
        font-weight: 600;
        color: #1a1a2e;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .header p {
        font-size: 1rem;
        color: #6b7280;
        margin: 0.3rem 0 0 0;
    }
    /* Caixa de resposta */
    .resposta-box {
        background-color: #f8f9fc;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #2563eb;
        margin: 1rem 0;
        line-height: 1.6;
        color: #1f2937;
    }
    .resposta-box strong {
        color: #1e40af;
    }
    /* Fonte */
    .fonte-box {
        background-color: #f1f5f9;
        padding: 0.8rem 1rem;
        border-radius: 6px;
        font-size: 0.85rem;
        color: #475569;
        margin-top: 0.5rem;
        border: 1px solid #e2e8f0;
    }
    /* Sidebar */
    .sidebar-section {
        background-color: #f8fafc;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1.2rem;
        border: 1px solid #e2e8f0;
    }
    .sidebar-section h4 {
        color: #1e293b;
        font-weight: 600;
        margin: 0 0 0.5rem 0;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .doc-item {
        padding: 0.3rem 0;
        font-size: 0.9rem;
        color: #334155;
        border-bottom: 1px solid #f1f5f9;
    }
    .doc-item:last-child {
        border-bottom: none;
    }
    /* Botão */
    .stButton button {
        background-color: #2563eb;
        color: white;
        font-weight: 500;
        border-radius: 6px;
        border: none;
        padding: 0.5rem 2rem;
        transition: all 0.2s;
    }
    .stButton button:hover {
        background-color: #1d4ed8;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    }
    /* Input */
    .stTextInput input {
        border-radius: 6px;
        border: 1px solid #d1d5db;
        padding: 0.6rem 1rem;
    }
    .stTextInput input:focus {
        border-color: #2563eb;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
    }
    /* Alertas */
    .success-box {
        background-color: #ecfdf5;
        color: #065f46;
        padding: 0.8rem 1rem;
        border-radius: 6px;
        border-left: 4px solid #10b981;
    }
    .error-box {
        background-color: #fef2f2;
        color: #991b1b;
        padding: 0.8rem 1rem;
        border-radius: 6px;
        border-left: 4px solid #ef4444;
    }
    /* Footer */
    .footer {
        text-align: center;
        color: #9ca3af;
        font-size: 0.8rem;
        padding: 1.5rem 0 0.5rem 0;
        border-top: 1px solid #e5e7eb;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Cabeçalho
st.markdown("""
<div class="header">
    <h1>Agente Inteligente</h1>
    <p>Assistente para consulta de documentos técnicos</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### Documentos")
    
    if os.path.exists("./data"):
        docs = os.listdir("./data")
        if docs:
            st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
            for doc in docs:
                st.markdown(f'<div class="doc-item">📄 {doc}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("Nenhum documento encontrado")
    else:
        st.warning("Pasta data/ não existe")
    
    st.divider()
    
    st.markdown("### Sobre")
    st.markdown(
        """
        <div style="font-size:0.85rem; color:#6b7280; line-height:1.5;">
        Este agente utiliza:
        <ul style="margin-top:0.3rem; padding-left:1.2rem;">
            <li>LangChain para orquestração</li>
            <li>Cohere para geração de texto</li>
            <li>ChromaDB para busca vetorial</li>
            <li>Streamlit para interface</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

# Carregar agente
@st.cache_resource
def carregar_agente():
    return AgenteInteligente()

try:
    with st.spinner("Carregando agente..."):
        agente = carregar_agente()
    
    if agente and agente.base.vector_store:
        st.markdown('<div class="success-box">Agente carregado com sucesso</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="error-box">Nenhum documento encontrado. Adicione arquivos na pasta data/</div>', unsafe_allow_html=True)
        st.stop()
except Exception as e:
    st.markdown(f'<div class="error-box">Erro: {str(e)}</div>', unsafe_allow_html=True)
    st.stop()

# Área principal
pergunta = st.text_input(
    "Digite sua pergunta:",
    placeholder="Exemplo: Quais são os principais algoritmos de machine learning?",
    key="pergunta_input"
)

if st.button("Perguntar", type="primary", use_container_width=True):
    if pergunta:
        with st.spinner("Processando..."):
            try:
                resposta = agente.perguntar(pergunta)
                
                st.markdown("### Resposta")
                st.markdown(f'<div class="resposta-box">{resposta}</div>', unsafe_allow_html=True)
                
                # Histórico
                if "historico" not in st.session_state:
                    st.session_state.historico = []
                st.session_state.historico.append({
                    "pergunta": pergunta,
                    "resposta": resposta
                })
                
            except Exception as e:
                st.markdown(f'<div class="error-box">Erro ao processar: {str(e)}</div>', unsafe_allow_html=True)
    else:
        st.warning("Digite uma pergunta")

# Histórico na sidebar
with st.sidebar:
    st.divider()
    st.markdown("### Histórico")
    
    if "historico" in st.session_state and st.session_state.historico:
        for i, item in enumerate(reversed(st.session_state.historico[-5:])):
            with st.expander(f"Pergunta {len(st.session_state.historico)-i}"):
                st.write(f"**P:** {item['pergunta']}")
                st.write(f"**R:** {item['resposta'][:120]}...")
    else:
        st.caption("Nenhuma pergunta realizada")

# Footer
st.markdown('<div class="footer">Desenvolvido com LangChain, Cohere e Streamlit</div>', unsafe_allow_html=True)