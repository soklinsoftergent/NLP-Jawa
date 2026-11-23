import re

# Read your raw file
with open("combined.txt", "r", encoding="utf-8") as f:
    text = f.read()

# --- Remove obvious URLs / web links ---
text = re.sub(r"https?://\S+", " ", text)  # http:// or https://
text = re.sub(r"www\.\S+", " ", text)      # www.something
text = re.sub(r"\b\S+\.(com|org|net|id|co|go|edu|gov|nl|uk|de|fr|jp|my|sg|io)\b\S*", " ", text)

# --- Remove HTML/XML tags ---
text = re.sub(r"<[^>]+>", " ", text)

# --- Remove digits and non-alphabetic symbols ---
cleaned = re.sub(
    r"[^a-zA-Záàâăäãĕéèêëíìîïóòôöõúùûüñčćšžøåāēīōū\s\n]",
    " ",
    text
)

# --- Remove digits explicitly (redundant safety) ---
cleaned = re.sub(r"\d+", " ", cleaned)

# --- Normalize whitespace ---
cleaned = re.sub(r"[ \t]+", " ", cleaned)      # collapse spaces/tabs
cleaned = re.sub(r"\n\s*\n+", "\n", cleaned)   # remove too many blank lines
cleaned = cleaned.strip().lower()

# --- Remove stray single-letter words ---
# Keep only 'a' and 'i' if they might be real words, otherwise remove all
cleaned = re.sub(r"\b[b-hj-z]\b", " ", cleaned)  # remove single letters except 'a' and 'i'

# Normalize spaces again after deletion
cleaned = re.sub(r"\s+", " ", cleaned).strip()

# --- Optionally wrap long lines for readability (100 words per line) ---
words = cleaned.split()
lines = []
for i in range(0, len(words), 100):
    lines.append(" ".join(words[i:i+100]))

formatted = "\n".join(lines)

# --- Save cleaned version ---
with open("cleans/javanese_clean.txt", "w", encoding="utf-8") as f:
    f.write(formatted)

print("✅ Cleaning done! Output saved to javanese_clean.txt")
