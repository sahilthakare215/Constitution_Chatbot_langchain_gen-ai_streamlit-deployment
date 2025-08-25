# Constitution Chatbot – LangChain + RAG (FastAPI + Streamlit)

This starter turns your Colab notebook into a simple **web UI** and **API**.

Two ways to run:
1) **Easiest (no separate backend):** Streamlit directly calls the RAG pipeline.
2) **API + UI:** FastAPI backend (`/ask`) + any frontend.

---

## 0) Prereqs
- Python 3.10+
- Your constitution PDF at `data/constitution.pdf`
- A Google Gemini API key in `GOOGLE_API_KEY`

---

## 1) Create & activate a virtual env (optional but recommended)

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

## 2) Install dependencies

```bash
pip install -r requirements.txt
```

## 3) Put your PDF
Copy your constitution PDF into `data/constitution.pdf`. (You can rename and update `PDF_PATH` in `.env` if needed.)

## 4A) Run Streamlit (no backend, simplest)

```bash
# Load your env vars (optional if you set them in shell)
cp .env.example .env  # then put your GOOGLE_API_KEY in .env
streamlit run ui_streamlit.py
```

Open the local URL Streamlit prints. Type a question and get an answer.

---

## 4B) Run FastAPI backend + (optional) simple HTML UI

### Start the API
```bash
# Ensure env vars are set (either via .env or shell)
uvicorn app_fastapi:app --host 0.0.0.0 --port 8000
```
- Test quickly with curl:
```bash
curl -X POST http://127.0.0.1:8000/ask -H "Content-Type: application/json" -d '{"question":"Can a constable arrest me?"}'
```

### (Optional) Open the minimal web UI
Just open `public/index.html` in your browser. It calls `http://127.0.0.1:8000/ask`.

If your API runs on another host (e.g., Render/Cloud Run), change `API_URL` inside `public/index.html`.

---

## 5) Deploy (two easy paths)

### A) Hugging Face Spaces (Streamlit only)
- Create a new Space → type **Streamlit**
- Upload these files (at minimum: `ui_streamlit.py`, `rag_pipeline.py`, `requirements.txt`, `data/constitution.pdf`)
- In the Space **Secrets**, set `GOOGLE_API_KEY`
- Space will build and run automatically

### B) Render (FastAPI)
- Push this folder to GitHub
- Create a new **Web Service** on Render
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app_fastapi:app --host 0.0.0.0 --port $PORT`
- Set Environment Variables: `GOOGLE_API_KEY`, `PDF_PATH` (optional)
- After deploy, you’ll get a public URL like `https://your-app.onrender.com/ask`

---

### Notes
- Your original notebook hard-coded an API key. Here we use **env vars**. Put your key in `.env` or your deploy provider's env settings.
- If you change `gemini-1.5-flash` to `gemini-1.5-pro`, remember that costs and latency differ.
- For larger PDFs, consider saving/loading FAISS index from disk to avoid rebuilding on every start.
