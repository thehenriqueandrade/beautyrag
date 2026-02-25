import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="BeautyRAG — Consultora de Marketing",
    page_icon="💅",
    layout="centered"
)

st.title("💅 BeautyRAG")
st.subheader("Sua consultora de marketing especializada em profissionais de beleza")
st.markdown("---")

st.markdown("""
**Exemplos de perguntas:**
- Como responder um cliente que pergunta o preço no WhatsApp?
- Como criar um carrossel no Instagram que venda sem parecer propaganda?
- Como comunicar aumento de preço sem perder clientes?
""")

question = st.text_area(
    "💬 Qual é a sua dúvida?",
    placeholder="Ex: Como captar mais clientes novas pelo Instagram?",
    height=100
)

if st.button("Perguntar", type="primary"):
    if not question.strip():
        st.warning("Digite uma pergunta antes de continuar.")
    else:
        with st.spinner("Consultando a base de conhecimento..."):
            try:
                response = requests.post(
                    f"{API_URL}/api/v1/ask",
                    json={"question": question, "max_results": 4},
                    timeout=30
                )
                data = response.json()

                st.markdown("### 📋 Resposta")
                st.write(data["answer"])

                with st.expander("📂 Fontes utilizadas"):
                    for source in data["sources"]:
                        st.markdown(f"- `{source}`")

                col1, col2 = st.columns(2)
                col1.metric("⏱️ Tempo de resposta", f"{data['latency_ms']} ms")
                col2.metric("🔤 Tokens estimados", data["tokens_used"])

            except Exception as e:
                st.error(f"Erro ao consultar a API: {e}")

st.markdown("---")
st.caption("BeautyRAG · Projeto de portfólio · RAG + FastAPI + ChromaDB")