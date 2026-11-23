# pdf_to_text_fixed.py
import fitz  # PyMuPDF
import re
import unicodedata

input_pdf = "resources/Babad Tanah Jawi.pdf"
output_txt = "kumpulan_corpora/output.txt"

def normalize_text(text):
    # Normalize Unicode composition (so ê = e + ̂ )
    text = unicodedata.normalize("NFC", text)
    
    # Fix common PDF extraction artifacts
    replacements = {
        "~": "ê",
        "ˆ": "ê",
        "´": "é",
        "`": "è",
        "˝": "ô",
        "˚": "o",
        "ˇ": "â",
        "¯": "ā",
        "˘": "ă",
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)

    # Remove weird double spaces, line breaks, etc.
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)
    text = text.strip()

    return text

with fitz.open(input_pdf) as doc:
    pages = [page.get_text("text") for page in doc]

cleaned = "\n".join(normalize_text(page) for page in pages)

with open(output_txt, "w", encoding="utf-8") as f:
    f.write(cleaned)

print("✅ Extracted and normalized text saved to", output_txt)
