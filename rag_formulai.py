# rag_formulai.py
import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import ollama

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load enriched text chunks (with metadata)
with open("faiss_index/formulai_enriched_chunks.json", "r") as f:
    enriched_chunks = json.load(f)

# Extract plain texts for embedding (if needed elsewhere)
texts = [chunk["text"] for chunk in enriched_chunks]

# Load full FAISS index (for unfiltered fallback, optional)
index = faiss.read_index("faiss_index/formulai.index")

def retrieve_similar_chunks(query: str, top_k: int = 5, product_type: str = None, skin_type: str = None):
    # Step 1: Filter by metadata
    filtered = []
    for i, chunk in enumerate(enriched_chunks):
        meta = chunk.get("metadata", {})
        if product_type and meta.get("product_type") != product_type:
            continue
        if skin_type and meta.get("skin_type") != skin_type:
            continue
        filtered.append((i, chunk["text"]))

    # If nothing matches, optionally fallback to all
    if not filtered:
        return []

    # Step 2: Embed query and compare only against filtered chunks
    query_embedding = model.encode([query])
    subset_texts = [text for _, text in filtered]
    subset_embeddings = model.encode(subset_texts)

    # Step 3: Temporary FAISS index on filtered subset
    dim = subset_embeddings[0].shape[0]
    temp_index = faiss.IndexFlatL2(dim)
    temp_index.add(np.array(subset_embeddings))
    distances, indices = temp_index.search(np.array(query_embedding), min(top_k, len(subset_texts)))

    # Step 4: Map back to enriched_chunks by original index
    return [enriched_chunks[filtered[i][0]] for i in indices[0]]

def build_prompt(query: str, context: str) -> str:
    return f"""
You are a senior cosmetic formulator at a top-tier laboratory.

### Task
Formulate a cosmetic product based on the following user brief.

**User Brief:** {query}

### Constraints:
- Use realistic, commonly accepted cosmetic ingredients
- Show all ingredients grouped by formulation phase (A, B, etc.)
- Output should total close to 100% (e.g. 99–100%)
- Use INCI names and optionally trade/common names
- Ensure safe usage levels, skin compatibility, and functional balance

### Reference Formulas:
{context}

### Output Format:
Phase A:
- INCI Name (Trade Name): %w/w
...

Phase B:
...

### Begin:
""".strip()

def generate_formula_with_ollama(query: str, retrieved_chunks: list, model_name: str = "llama3"):
    context = "\n\n".join(chunk["text"] for chunk in retrieved_chunks)
    full_prompt = build_prompt(query, context)

    response = ollama.chat(
        model=model_name,
        messages=[{"role": "user", "content": full_prompt}]
    )
    return response['message']['content'], context
