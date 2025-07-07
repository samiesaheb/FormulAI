# 🧪 FormulAI – AI-Powered Cosmetic Formulation Assistant

FormulAI is an **AI-driven assistant designed to help cosmetic scientists and product developers create effective, safe, and customized cosmetic product formulas**. By leveraging advanced Retrieval-Augmented Generation (RAG) techniques, FormulAI combines a database of real-world cosmetic formulations with powerful local large language models to generate ingredient- and phase-aware formulas tailored to specific product and skin types.

---

## ✨ Key Features

- 🧠 **Retrieval-Augmented Generation (RAG):** Uses a vector search (FAISS) over past cosmetic formulas to provide relevant context for formula generation.
- 🔍 **Filtered Retrieval:** Search and retrieve formulas by product type (e.g., moisturizer, serum) and skin type (e.g., oily, sensitive).
- 🤖 **Local Large Language Model Generation:** Generates new formulations using local LLMs such as LLaMA 3 via Ollama for privacy and speed.
- 📦 **Structured Output:** Exports generated formulas in CSV format with ingredient and phase information for easy integration.
- 🧪 **Ingredient- and Phase-Aware:** Ensures generated formulas respect cosmetic formulation best practices.
- 🖥 **Interactive UI:** Built with Streamlit for an intuitive and user-friendly experience.

---

## 🚀 Getting Started

Follow these steps to set up and run FormulAI locally:

### Prerequisites

- Python 3.8+
- [Ollama](https://ollama.com) installed and running
- Model pulled locally via Ollama (e.g., `ollama pull llama3`)

### Installation

git clone https://github.com/your-username/FormulAI.git
cd FormulAI

python3 -m venv venv
source venv/bin/activate # On Windows use venv\Scripts\activate
pip install -r requirements.txt


### Data Preparation

Generate vector embeddings and index chunks for retrieval:

python generate_chunks.py


### Running the Application

Start the Streamlit app:

streamlit run app.py


Make sure Ollama is running and the desired LLM model is available locally.

---

## 🛠 Technology Stack

| Component           | Technology/Library                      |
|---------------------|---------------------------------------|
| Large Language Model | Ollama (LLaMA 3, Mistral, etc.)       |
| Embeddings          | Sentence-Transformers (all-MiniLM-L6-v2) |
| Vector Store        | FAISS (local vector similarity search) |
| User Interface      | Streamlit                             |
| Data Source         | CSV files of real cosmetic formulations |

---

## 🔍 How It Works

FormulAI uses a **Retrieval-Augmented Generation** approach:

1. **Embedding & Indexing:** Past cosmetic formulas are embedded using Sentence-Transformers and indexed with FAISS.
2. **Context Retrieval:** When a user specifies product and skin type, relevant formulas are retrieved from the index.
3. **Generation:** The retrieved context is fed into a local LLM (via Ollama) to generate a new, customized formula.
4. **Output:** The generated formula is presented in an ingredient- and phase-aware format and can be exported as CSV.

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request for bug fixes, improvements, or new features.

---

## 📞 Contact

For questions or collaboration, please contact [your-email@example.com].

---

## 📚 References & Resources

- [Ollama](https://ollama.com)
- [FAISS](https://github.com/facebookresearch/faiss)
- [Sentence-Transformers](https://www.sbert.net/)
- [Streamlit](https://streamlit.io)

---

*FormulAI empowers cosmetic formulation with AI, combining domain knowledge and cutting-edge NLP to accelerate product innovation.*
