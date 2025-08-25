import os
import streamlit as st
from rag_pipeline import RAGBot

st.set_page_config(page_title="Constitution Chatbot", page_icon="📘")
st.title("📘 Constitution Chatbot")

# Hardcode the correct PDF path
PDF_PATH = "constitution-chatbot-starter/data/20240716890312078.pdf"

# Initialize the bot once
if "bot" not in st.session_state:
    try:
        st.session_state.bot = RAGBot(pdf_path=PDF_PATH)
    except Exception as e:
        st.error(f"Error initializing bot: {str(e)}")
        st.stop()

st.markdown("### Ask a question about the constitution")

# Simple question input
q = st.text_input("Your question:", placeholder="e.g., What are the fundamental rights?")

if st.button("Get Answer") and q:
    bot = st.session_state.get("bot")
    if not bot:
        st.error("Bot is not initialized. Please check your Google API key.")
    else:
        with st.spinner("Thinking..."):
            try:
                out = bot.ask(q)
                st.markdown("### Answer")
                st.write(out["answer"] or "No answer found.")
                
                # Removed expander sections for articles and sources
                        
            except Exception as e:
                st.error(f"Error getting answer: {str(e)}")

st.caption("Powered by Google Gemini via LangChain. Requires GOOGLE_API_KEY in environment.")
