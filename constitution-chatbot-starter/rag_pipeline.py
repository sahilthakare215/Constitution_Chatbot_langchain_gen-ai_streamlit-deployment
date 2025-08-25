import os
import re
from typing import Dict, List
from dotenv import load_dotenv
import streamlit as st  # Import Streamlit for UI updates

from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA

class RAGBot:
    """
    Minimal RAG bot that loads a PDF, chunks it, builds a FAISS index,
    and answers questions using Gemini via LangChain.
    """
    def __init__(self, pdf_path: str | None = None, google_api_key: str | None = None):
        load_dotenv()  # load .env if present

        pdf_path = pdf_path or os.getenv("PDF_PATH", "data/constitution.pdf")
        google_api_key = google_api_key or os.getenv("GOOGLE_API_KEY")

        if not google_api_key:
            raise RuntimeError("Missing GOOGLE_API_KEY. Put it in environment or .env file.")
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found at {pdf_path}. Update PDF_PATH or place the file there.")

        # Ensure environment variable for Google libs
        os.environ["GOOGLE_API_KEY"] = google_api_key

        # 1) Read PDF only once and cache the text
        print("Loading PDF...")
        if not hasattr(self, 'cached_text'):
            self.cached_text = ""
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                self.cached_text += (page.extract_text() or "") + "\n"

        # 2) Chunk text
        splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=200)
        docs = splitter.create_documents([self.cached_text], metadatas=[{"source": os.path.basename(pdf_path)}])

        self.embeddings = None  # Initialize as None
        self.vs = None  # Initialize as None

        # 4) LLM
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)

        # Load embeddings and vector store if not already loaded
        if self.embeddings is None or self.vs is None:
            with st.spinner("Loading embeddings and vector store..."):
                try:
                    self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
                    self.vs = FAISS.from_documents(docs, self.embeddings)
                    st.success("Embeddings and vector store initialized successfully.")
                except Exception as e:
                    st.error(f"Error initializing embeddings or vector store: {e}")
                    raise

        # Initialize the chain after embeddings and vector store are set
        self.chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vs.as_retriever(search_kwargs={"k": 4}),
            return_source_documents=True
        )
        st.success("RetrievalQA chain initialized successfully.")

    def ask(self, question: str) -> Dict:
        """
        Returns: {"answer": str, "articles": List[str], "sources": List[str]}
        """
        # Enhance question context for better retrieval
        enhanced_question = question
        if any(keyword in question.lower() for keyword in ['arrest', 'police', 'constable', 'detain']):
            enhanced_question = f"{question} constitutional rights arrest procedures fundamental rights"
        
        result = self.chain.invoke({"query": enhanced_question})
        answer = (result.get("result") or "").strip()
        src_docs = result.get("source_documents") or []

        sources: List[str] = []
        for d in src_docs:
            meta = getattr(d, "metadata", {}) or {}
            src = meta.get("source", "")
            if src:
                sources.append(src)

        # Try to detect "Article N" mentions in the answer itself
        articles = re.findall(r"(?:Article|Art\.)\s*\d+", answer, flags=re.IGNORECASE)
        articles = sorted(set(a.title() for a in articles))

        # If answer is vague, provide more helpful response
        if "don't know" in answer.lower() or "no answer" in answer.lower() or "not contain" in answer.lower():
            answer = f"I cannot find specific information about '{question}' in the Indian Constitution. However, the Constitution does contain provisions about arrest procedures and fundamental rights (particularly Article 22). For specific police powers and arrest procedures, you may need to consult the Code of Criminal Procedure or relevant police manuals."
        
        # Add a more detailed explanation
        explanation = "In the context of constitutional law, it's important to understand the principles that govern individual rights and law enforcement procedures. The Constitution outlines various rights that protect citizens, including the right to legal counsel and protection against arbitrary arrest."
        answer += f"\n\nExplanation: {explanation}"

        return {"answer": answer, "articles": articles, "sources": sorted(set(sources))}
