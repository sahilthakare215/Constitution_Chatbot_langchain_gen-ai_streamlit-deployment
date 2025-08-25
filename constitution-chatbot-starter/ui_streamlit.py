import os
import streamlit as st
from rag_pipeline import RAGBot

st.set_page_config(page_title="Constitution Chatbot", page_icon="📘")
st.title("📘 Constitution Chatbot (LangChain + RAG)")

with st.sidebar:
    st.markdown("### Settings")
    default_pdf = os.getenv("PDF_PATH", "data/constitution.pdf")
    pdf_path = st.text_input("PDF path", value=default_pdf)
    st.caption("Put your PDF at the path above. Default: data/constitution.pdf")

if "bot" not in st.session_state or st.session_state.get("pdf_path") != pdf_path:
    try:
        st.session_state.bot = RAGBot(pdf_path=pdf_path)
        st.session_state.pdf_path = pdf_path
    except Exception as e:
        st.error(str(e))

q = st.text_input("Ask a question")
if st.button("Ask") and q:
    bot = st.session_state.get("bot")
    if not bot:
        st.error("Bot is not initialized.")
    else:
        with st.spinner("Thinking..."):
            out = bot.ask(q)
        st.markdown("#### Answer")
        st.write(out["answer"] or "No answer.")
        if out["articles"]:
            st.markdown("#### Detected Articles")
            st.write(", ".join(out["articles"]))
        if out["sources"]:
            st.markdown("#### Sources")
            st.write(", ".join(out["sources"]))
st.caption("Uses Gemini via LangChain. Set GOOGLE_API_KEY in your environment or .env file.")
