# 🧪 FormulAI – AI-Powered Cosmetic Formulation Assistant

FormulAI is an AI-driven tool that helps cosmetic scientists and product developers generate effective, safe cosmetic product formulas. It uses a Retrieval-Augmented Generation (RAG) pipeline with FAISS for vector search, Hugging Face for embeddings, and Ollama for local large language model generation.

---

## ✨ Features

- 🧠 **Retrieval-Augmented Generation** using past formulas as context
- 🔍 Filtered retrieval by product type and skin type
- 🤖 Local LLM generation via Ollama (e.g. LLaMA 3)
- 📦 CSV export of structured formulas
- 🧪 Ingredient and phase-aware output format
- 🖥 Built with Streamlit for interactive UI

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/FormulAI.git
cd FormulAI

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python generate_chunks.py

streamlit run app.py

Make sure Ollama is running and that you’ve pulled a model like:

ollama pull llama3
```
🛠 Tech Stack
LLM: Ollama (LLaMA 3, Mistral, etc.)

Embedding: Sentence-Transformers (all-MiniLM-L6-v2)

Vector Store: FAISS (local)

UI: Streamlit

Data: CSV of real cosmetic formulations

📄 License
MIT License. See LICENSE for details.
