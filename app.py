# app.py
import streamlit as st
import pandas as pd
import io
import re
from rag_formulai import retrieve_similar_chunks, generate_formula_with_ollama

st.set_page_config(page_title="FormulAI", layout="centered")
st.title("🧪 FormulAI — AI Cosmetic Formula Generator")

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.markdown("Using model: `llama3`")
    top_k = st.slider("Number of retrieved formulas", 3, 10, 5)

    product_type = st.selectbox("Product Type Filter", ["", "serum", "shampoo", "lotion"])
    skin_type = st.selectbox("Skin Type Filter", ["", "all", "dry", "oily"])

# Input
query = st.text_input("Enter product brief", placeholder="e.g. gentle shampoo for dry scalp with aloe vera")

if st.button("Generate Formula") and query:
    with st.spinner("🔍 Retrieving relevant formulas..."):
        chunks = retrieve_similar_chunks(
            query,
            top_k=top_k,
            product_type=product_type if product_type else None,
            skin_type=skin_type if skin_type else None
        )

    if chunks:
        with st.expander("🔎 Retrieved Relevant Formulas"):
            for i, c in enumerate(chunks):
                st.markdown(f"**Match {i+1}**")
                st.code(c["text"], language="markdown")
                st.caption(f"Product Type: {c['metadata'].get('product_type')}, Skin Type: {c['metadata'].get('skin_type')}")
    else:
        st.warning("No matching formulas found for selected filters.")

    with st.spinner("🤖 Generating formula using Ollama..."):
        output, full_context = generate_formula_with_ollama(query, chunks, model_name="llama3")

    st.markdown("### 🧴 Generated Formula")
    st.code(output, language="markdown")

    with st.expander("📄 Full Prompt Sent to Ollama"):
        st.text_area("Prompt", value=full_context, height=300)

    # --- CSV Export ---
    def parse_generated_formula(text):
        rows = []
        current_phase = ""
        for line in text.splitlines():
            phase_match = re.match(r"Phase\s+([A-Z])", line.strip())
            item_match = re.match(r"-?\s*(.+?)\s*\((.+?)\):\s*([\d.]+)%", line.strip())

            if phase_match:
                current_phase = phase_match.group(1)
            elif item_match:
                inci = item_match.group(1).strip()
                name = item_match.group(2).strip()
                percent = float(item_match.group(3))
                rows.append({"Phase": current_phase, "INCI": inci, "%w/w": percent})

        return pd.DataFrame(rows)

    df_formula = parse_generated_formula(output)

    if not df_formula.empty:
        st.markdown("### 📤 Export Formula")
        buffer = io.StringIO()
        df_formula.to_csv(buffer, index=False)
        st.download_button(
            label="Download Formula as CSV",
            data=buffer.getvalue(),
            file_name="generated_formula.csv",
            mime="text/csv"
        )
