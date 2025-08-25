# Constitution Chatbot – Streamlit Version

This project is a Constitution Chatbot that utilizes Retrieval-Augmented Generation (RAG) with a Streamlit interface.

## 📋 Overview
The Constitution Chatbot allows users to ask questions about constitutional documents and receive AI-powered answers based on a provided PDF. Built with Streamlit, LangChain, and Google Gemini.

## 🎯 Files Required for Streamlit Deployment

### Essential Files:
- `ui_streamlit.py` - Main Streamlit application with configurable settings
- `ui_streamlit_simple.py` - Simplified Streamlit version (hardcoded PDF path)
- `rag_pipeline.py` - Core RAG functionality using LangChain
- `requirements.txt` - Python dependencies
- `data/constitution.pdf` - Your constitution PDF document
- `.env` or `.env.example` - Environment variables configuration

### Optional Files (Not needed for Streamlit):
- `app_fastapi.py` - FastAPI backend (for API-only deployment)
- `public/index.html` - HTML frontend for FastAPI (not used with Streamlit)

## 🚀 Prerequisites
- **Python 3.10+**
- **Google Gemini API key** (set as `GOOGLE_API_KEY` environment variable)
- **Constitution PDF** placed at `data/constitution.pdf`

## ⚡ Quick Start

1. **Create virtual environment**:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your GOOGLE_API_KEY
   ```

4. **Place your PDF**:
   Copy your constitution PDF to `data/constitution.pdf`

5. **Run the application**:
   ```bash
   # Main version (with configurable PDF path):
   streamlit run ui_streamlit.py
   
   # Simple version (hardcoded path):
   streamlit run ui_streamlit_simple.py
   ```

## 🎮 Usage
- Open the local URL provided by Streamlit
- Type your constitutional law question in the input field
- Click "Ask" or "Get Answer" to receive AI-generated responses
- View detected articles and sources in the response

## ✨ Features
- **PDF Processing**: Automatic text extraction and chunking
- **Semantic Search**: FAISS vector store for efficient retrieval
- **AI-Powered Answers**: Google Gemini for natural language understanding
- **Source Attribution**: References to specific articles and sources
- **Configurable UI**: Sidebar settings for PDF path configuration

## 🌐 Deployment - Hugging Face Spaces

### Required Files to Upload:
- `ui_streamlit.py` (or `ui_streamlit_simple.py`)
- `rag_pipeline.py`
- `requirements.txt`
- Your PDF file (e.g., `data/constitution.pdf`)

### Steps:
1. Create a new **Streamlit** Space on Hugging Face
2. Upload the required files listed above
3. Set `GOOGLE_API_KEY` in Space **Secrets**
4. The Space will build and deploy automatically

## 🔧 Troubleshooting

### Common Issues:
1. **Missing API Key**: Ensure `GOOGLE_API_KEY` is set in environment or .env file
2. **PDF Not Found**: Verify the PDF is at the correct path (`data/constitution.pdf`)
3. **Dependency Issues**: Use Python 3.10+ and install all requirements

### Environment Variables:
```bash
GOOGLE_API_KEY=your_google_api_key_here
PDF_PATH=data/constitution.pdf  # Optional, defaults to data/constitution.pdf
```

## 🏗️ Technical Architecture
- **Frontend**: Streamlit for interactive web interface
- **RAG Pipeline**: LangChain for document processing and retrieval
- **Embeddings**: Google Generative AI embeddings
- **Vector Store**: FAISS for efficient similarity search
- **LLM**: Google Gemini for answer generation

## 📁 File Structure for Streamlit
```
constitution-chatbot-starter/
├── ui_streamlit.py          # Main Streamlit app
├── ui_streamlit_simple.py   # Simplified Streamlit app
├── rag_pipeline.py          # RAG functionality
├── requirements.txt         # Dependencies
├── .env                     # Environment variables
└── data/
    └── constitution.pdf     # Your PDF document
```

*Note: Files like `app_fastapi.py` and `public/index.html` are for FastAPI deployment and not required for Streamlit.*
