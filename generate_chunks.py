import pandas as pd
from collections import defaultdict
import json
import os

# Load your CSV
df = pd.read_csv("formulations_filled_parts.csv")

# Group by product_name and phase
grouped = df.groupby(["product_name", "Part"])

formulas = defaultdict(lambda: defaultdict(list))
for (product, part), group in grouped:
    for _, row in group.iterrows():
        formulas[product][part].append((row['INCI'], row['Ingredient'], row['%w/w']))

# Extract metadata
def extract_metadata(product_name, ingredients):
    lower_name = product_name.lower()
    product_type = "serum" if "serum" in lower_name else \
                   "shampoo" if "shampoo" in lower_name else \
                   "lotion" if "lotion" in lower_name else "unknown"

    skin_type = "oily" if "oily" in lower_name else \
                "dry" if "dry" in lower_name else "all"

    inci_list = [inci for inci, _, _ in ingredients]
    return {
        "product_name": product_name,
        "product_type": product_type,
        "skin_type": skin_type,
        "key_ingredients": inci_list
    }

# Generate enriched chunks
enriched_chunks = []

for product, parts in formulas.items():
    lines = [f"Formula: {product}"]
    ingredients_flat = []

    for part, ingredients in sorted(parts.items()):
        lines.append(f"Phase {part}:")
        for inci, ing_name, percent in ingredients:
            lines.append(f"- {inci} ({ing_name}): {percent}%")
            ingredients_flat.append((inci, ing_name, percent))

    chunk_text = "\n".join(lines)
    metadata = extract_metadata(product, ingredients_flat)

    enriched_chunks.append({
        "text": chunk_text,
        "metadata": metadata
    })

# Save to file
os.makedirs("faiss_index", exist_ok=True)
with open("faiss_index/formulai_enriched_chunks.json", "w") as f:
    json.dump(enriched_chunks, f, indent=2)

print("✅ Enriched chunks saved to: faiss_index/formulai_enriched_chunks.json")
